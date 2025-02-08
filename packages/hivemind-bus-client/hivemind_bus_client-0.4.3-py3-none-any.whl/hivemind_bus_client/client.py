import json
import ssl
from threading import Event
from typing import Union, Optional, Callable

import pybase64
from Cryptodome.PublicKey import RSA
from ovos_bus_client import Message as MycroftMessage, MessageBusClient as OVOSBusClient
from ovos_bus_client.session import Session
from ovos_utils.fakebus import FakeBus
from ovos_utils.log import LOG
from pyee import EventEmitter
from websocket import ABNF
from websocket import WebSocketApp, WebSocketConnectionClosedException

from hivemind_bus_client.identity import NodeIdentity
from hivemind_bus_client.message import HiveMessage, HiveMessageType
from hivemind_bus_client.serialization import HiveMindBinaryPayloadType
from hivemind_bus_client.serialization import get_bitstring, decode_bitstring
from hivemind_bus_client.util import serialize_message
from hivemind_bus_client.encryption import (encrypt_as_json, decrypt_from_json, encrypt_bin, decrypt_bin,
                                            SupportedEncodings, SupportedCiphers)
from poorman_handshake.asymmetric.utils import encrypt_RSA, load_RSA_key, sign_RSA


class BinaryDataCallbacks:
    def handle_receive_tts(self, bin_data: bytes,
                           utterance: str,
                           lang: str,
                           file_name: str):
        LOG.warning(f"Ignoring received binary TTS audio: {utterance} with {len(bin_data)} bytes")

    def handle_receive_file(self, bin_data: bytes,
                            file_name: str):
        LOG.warning(f"Ignoring received binary file: {file_name} with {len(bin_data)} bytes")


class HiveMessageWaiter:
    """Wait for a single message.

    Encapsulate the wait for a message logic separating the setup from
    the actual waiting act so the waiting can be setuo, actions can be
    performed and _then_ the message can be waited for.

    Arguments:
        bus: Bus to check for messages on
        message_type: message type to wait for
    """

    def __init__(self, bus: 'HiveMessageBusClient',
                 message_type: Union[HiveMessageType, str]):
        self.bus = bus
        self.msg_type = message_type
        self.received_msg = None
        # Setup response handler
        self.response_event = Event()
        self.bus.on(self.msg_type, self._handler)

    def _handler(self, message):
        """Receive response data."""
        self.received_msg = message
        self.response_event.set()

    def wait(self, timeout=3.0):
        """Wait for message.

        Arguments:
            timeout (int or float): seconds to wait for message

        Returns:
            HiveMessage or None
        """
        self.response_event.wait(timeout)
        self.bus.remove(self.msg_type, self._handler)
        return self.received_msg


class HivePayloadWaiter(HiveMessageWaiter):
    def __init__(self, bus: 'HiveMessageBusClient',
                 payload_type: Union[HiveMessageType, str],
                 message_type: Union[HiveMessageType, str] = HiveMessageType.BUS,
                 *args, **kwargs):
        super(HivePayloadWaiter, self).__init__(bus=bus, message_type=message_type,
                                                *args, **kwargs)
        self.payload_type = payload_type

    def _handler(self, message):
        """Receive response data."""
        if message.payload.msg_type == self.payload_type:
            super()._handler(message)


class HiveMessageBusClient(OVOSBusClient):
    def __init__(self, key: Optional[str] = None,
                 password: Optional[str] = None,
                 crypto_key: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 useragent: str = "",
                 self_signed: bool = True,
                 share_bus: bool = False,
                 compress: bool = True,
                 binarize: bool = True,
                 identity: NodeIdentity = None,
                 internal_bus: Optional[OVOSBusClient] = None,
                 bin_callbacks: BinaryDataCallbacks = BinaryDataCallbacks()):
        self.bin_callbacks = bin_callbacks
        self.json_encoding = SupportedEncodings.JSON_HEX  # server defaults before it was made configurable
        self.cipher = SupportedCiphers.AES_GCM  # server defaults before it was made configurable

        self.identity = identity or None
        self._password = password
        self._access_key = key
        self._name = useragent
        self._port = port
        self._host = host
        self.init_identity()

        self.crypto_key = crypto_key
        self.allow_self_signed = self_signed
        self.share_bus = share_bus
        self.handshake_event = Event()

        # if you want to reduce CPU usage in exchange for more bandwidth set below to False
        self.compress = compress  # None -> auto
        self.binarize = binarize  # only if hivemind reports also supporting it

        # connect to OVOS, if on a OVOS device
        if not internal_bus:
            # FakeBus needed to send emitted events to handlers registered within the client
            sess = Session()  # new session for this client
            self.internal_bus = FakeBus(session=sess)
        else:
            sess = Session(session_id=internal_bus.session_id)
            self.internal_bus = internal_bus
        LOG.info(f"Session ID: {sess.session_id}")

        # NOTE: self._host and self._port accessed only after self.init_identity()
        # this allows them to come from set-identity cli command
        use_ssl = self._host.startswith("wss://")
        host = self._host.replace("ws://", "").replace("wss://", "").strip()
        super().__init__(host=host, port=self._port, ssl=use_ssl,
                         emitter=EventEmitter(), session=sess)

    def init_identity(self, site_id=None):
        self.identity = self.identity or NodeIdentity()
        self.identity.password = self._password or self.identity.password
        self.identity.access_key = self._access_key or self.identity.access_key
        self.identity.default_master = self._host = self._host or self.identity.default_master
        self.identity.default_port = self._port = self._port or self.identity.default_port
        self.identity.name = self._name or "HiveMessageBusClientV0.0.1"
        self.identity.site_id = site_id or self.identity.site_id

        if not self.identity.access_key or not self.identity.password:
            raise RuntimeError("NodeIdentity not set, please pass key and password or "
                               "call 'hivemind-client set-identity'")
        if not self.identity.default_master:
            raise RuntimeError("host not set, please pass host and port or "
                               "call 'hivemind-client set-identity'")

    @property
    def useragent(self):
        return self.identity.name

    @useragent.setter
    def useragent(self, val):
        self.identity.name = val

    @property
    def password(self):
        return self.identity.password

    @property
    def key(self):
        return self.identity.access_key

    @property
    def site_id(self):
        return self.identity.site_id

    @site_id.setter
    def site_id(self, val):
        self.identity.site_id = val

    @password.setter
    def password(self, val):
        self.identity.password = val

    @key.setter
    def key(self, val):
        self.identity.access_key = val

    def connect(self, bus=FakeBus(), protocol=None, site_id=None):
        from hivemind_bus_client.protocol import HiveMindSlaveProtocol

        self.identity.site_id = site_id or self.identity.site_id

        if protocol is None:
            LOG.debug("Initializing HiveMindSlaveProtocol")
            self.protocol = HiveMindSlaveProtocol(self,
                                                  shared_bus=self.share_bus,
                                                  site_id=self.identity.site_id or "unknown",
                                                  identity=self.identity)
        else:
            self.protocol = protocol
            self.protocol.identity = self.identity
            if self.identity.site_id is not None:
                self.protocol.site_id = self.identity.site_id

        LOG.info("Connecting to Hivemind")
        self.run_in_thread()
        self.protocol.bind(bus)
        self.wait_for_handshake()

    def on_open(self, *args):
        """
        Handle the "open" event from the websocket.
        A Basic message with the name "open" is forwarded to the emitter.
        """
        LOG.debug("Connected")
        self.connected_event.set()
        self.emitter.emit("open")
        # Restore reconnect timer to 5 seconds on sucessful connect
        self.retry = 5

    def on_error(self, *args):
        self.handshake_event.clear()
        self.crypto_key = None
        super().on_error(*args)

    def on_close(self, *args):
        self.handshake_event.clear()
        self.crypto_key = None
        super().on_close(*args)

    def wait_for_handshake(self, timeout=5):
        self.handshake_event.wait(timeout=timeout)
        if not self.handshake_event.is_set():
            self.protocol.start_handshake()
            self.wait_for_handshake()

    @staticmethod
    def build_url(key, host='127.0.0.1', port=5678,
                  useragent="HiveMessageBusClientV0.0.1", ssl=True):
        scheme = 'wss' if ssl else 'ws'
        key = pybase64.b64encode(f"{useragent}:{key}".encode("utf-8")).decode("utf-8")
        return f'{scheme}://{host}:{port}?authorization={key}'

    def create_client(self):
        url = self.build_url(ssl=self.config.ssl,
                             host=self.config.host,
                             port=self.config.port,
                             key=self.key,
                             useragent=self.useragent)
        return WebSocketApp(url, on_open=self.on_open, on_close=self.on_close,
                            on_error=self.on_error, on_message=self.on_message)

    def run_forever(self):
        self.started_running = True
        if self.allow_self_signed:
            self.client.run_forever(sslopt={
                "cert_reqs": ssl.CERT_NONE,
                "check_hostname": False,
                "ssl_version": ssl.PROTOCOL_TLS_CLIENT})
        else:
            self.client.run_forever()

    # event handlers
    def on_message(self, *args):
        if len(args) == 1:
            message = args[0]
        else:
            message = args[1]
        if self.crypto_key:
            # handle binary encryption
            if isinstance(message, bytes):
                message = decrypt_bin(self.crypto_key, message, cipher=self.cipher)
            # handle json encryption
            elif "ciphertext" in message:
                # LOG.debug(f"got encrypted message: {len(message)}")
                message = decrypt_from_json(self.crypto_key, message,
                                            cipher=self.cipher, encoding=self.json_encoding)
            else:
                LOG.debug("Message was unencrypted")

        if isinstance(message, bytes):
            message = decode_bitstring(message)
        elif isinstance(message, str):
            message = json.loads(message)
        if isinstance(message, dict) and "ciphertext" in message:
            LOG.error("got encrypted message, but could not decrypt!")
            return

        if (isinstance(message, HiveMessage) and message.msg_type == HiveMessageType.BINARY):
            self._handle_binary(message)
            return

        if isinstance(message, HiveMessage):
            self.emitter.emit('message', message.serialize())  # raw message
            self._handle_hive_protocol(message)
        elif isinstance(message, str):
            self.emitter.emit('message', message)  # raw message
            self._handle_hive_protocol(HiveMessage(**json.loads(message)))
        else:
            assert isinstance(message, dict)
            self.emitter.emit('message', json.dumps(message, ensure_ascii=False))  # raw message
            self._handle_hive_protocol(HiveMessage(**message))

    def _handle_binary(self, message: HiveMessage):
        assert message.msg_type == HiveMessageType.BINARY
        bin_data = message.payload
        LOG.debug(f"Got binary data of type: {message.bin_type}")
        if message.bin_type == HiveMindBinaryPayloadType.TTS_AUDIO:
            lang = message.metadata.get("lang")
            utt = message.metadata.get("utterance")
            file_name = message.metadata.get("file_name")
            try:
                self.bin_callbacks.handle_receive_tts(bin_data, utt, lang, file_name)
            except:
                LOG.exception("Error in binary callback: handle_receive_tts")
        elif message.bin_type == HiveMindBinaryPayloadType.FILE:
            file_name = message.metadata.get("file_name")
            try:
                self.bin_callbacks.handle_receive_file(bin_data, file_name)
            except:
                LOG.exception("Error in binary callback: handle_receive_file")
        else:
            LOG.warning(f"Ignoring received untyped binary data: {len(bin_data)} bytes")

    def _handle_hive_protocol(self, message: HiveMessage):
        # LOG.debug(f"received HiveMind message: {message.msg_type}")
        if message.msg_type == HiveMessageType.BUS:
            self.internal_bus.emit(message.payload)
        self.emitter.emit(message.msg_type, message)  # hive message

    def emit(self, message: Union[MycroftMessage, HiveMessage],
             binary_type: HiveMindBinaryPayloadType = HiveMindBinaryPayloadType.UNDEFINED):
        if isinstance(message, MycroftMessage):
            message = HiveMessage(msg_type=HiveMessageType.BUS,
                                  payload=message)
        if not self.connected_event.is_set():
            LOG.warning("hivemind connection not ready")
            if not self.connected_event.wait(10):
                if not self.started_running:
                    raise ValueError('You must execute run_forever() '
                                     'before emitting messages')
                self.connected_event.wait()

        try:
            # auto inject context for proper routing, this is confusing for
            # end users if they need to do it manually, error prone and easy
            # to forget
            if message.msg_type == HiveMessageType.BUS:
                ctxt = dict(message.payload.context)
                if "source" not in ctxt:
                    ctxt["source"] = self.useragent
                if "platform" not in message.payload.context:
                    ctxt["platform"] = self.useragent
                if "destination" not in message.payload.context:
                    ctxt["destination"] = "HiveMind"
                if "session" not in ctxt:
                    ctxt["session"] = {}
                ctxt["session"]["session_id"] = self.session_id
                ctxt["session"]["site_id"] = self.site_id
                message.payload.context = ctxt
                # also send event to client registered handlers
                self.internal_bus.emit(message.payload)

            LOG.debug(f"sending to HiveMind: {message.msg_type}")
            binarize = False
            if message.msg_type == HiveMessageType.BINARY:
                binarize = True
            elif message.msg_type not in [HiveMessageType.HELLO, HiveMessageType.HANDSHAKE]:
                binarize = self.protocol.binarize and self.binarize

            if binarize:
                bitstr = get_bitstring(hive_type=message.msg_type,
                                       payload=message.payload,
                                       compressed=self.compress,
                                       binary_type=binary_type,
                                       hivemeta=message.metadata)
                if self.crypto_key:
                    ws_payload = encrypt_bin(self.crypto_key, bitstr.bytes, cipher=self.cipher)
                else:
                    ws_payload = bitstr.bytes
                self.client.send(ws_payload, ABNF.OPCODE_BINARY)
            else:
                ws_payload = serialize_message(message)
                if self.crypto_key:
                    ws_payload = encrypt_as_json(self.crypto_key, ws_payload,
                                                 cipher=self.cipher, encoding=self.json_encoding)
                self.client.send(ws_payload)

        except WebSocketConnectionClosedException:
            LOG.warning(f'Could not send {message.msg_type} message because connection '
                        'has been closed')

    def emit_mycroft(self, message: MycroftMessage):
        message = HiveMessage(msg_type=HiveMessageType.BUS, payload=message)
        self.emit(message)

    def on_mycroft(self, mycroft_msg_type, func):
        LOG.debug(f"registering mycroft event: {mycroft_msg_type}")
        self.internal_bus.on(mycroft_msg_type, func)

    # event api
    def on(self, event_name, func):
        if event_name not in list(HiveMessageType):
            # assume it's a mycroft message
            # this could be done better,
            # but makes this lib almost a drop in replacement
            # for the mycroft bus client
            # LOG.info(f"registering mycroft handler: {event_name}")
            self.on_mycroft(event_name, func)
        else:
            # hivemind message
            LOG.debug(f"registering handler: {event_name}")
            self.emitter.on(event_name, func)

    def remove(self, event_name: str, func: Callable):
        if event_name not in list(HiveMessageType):
            self.internal_bus.remove(event_name, func)
        else:  # hivemind message
            self.emitter.remove_listener(event_name, func)

    # utility
    def wait_for_message(self, message_type: Union[HiveMessageType, str], timeout=3.0):
        """Wait for a message of a specific type.

        Arguments:
            message_type (HiveMessageType): the message type of the expected message
            timeout: seconds to wait before timeout, defaults to 3

        Returns:
            The received message or None if the response timed out
        """

        return HiveMessageWaiter(self, message_type).wait(timeout)

    def wait_for_payload(self, payload_type: Union[HiveMessageType, str],
                         message_type: Union[HiveMessageType, str] = HiveMessageType.THIRDPRTY,
                         timeout=3.0):
        """Wait for a message of a specific type + payload of a specific type.

        Arguments:
            payload_type (str): the message type of the expected payload
            message_type (HiveMessageType): the message type of the expected message
            timeout: seconds to wait before timeout, defaults to 3

        Returns:
            The received message or None if the response timed out
        """

        return HivePayloadWaiter(bus=self, payload_type=payload_type,
                                 message_type=message_type).wait(timeout)

    def wait_for_mycroft(self, mycroft_msg_type: str, timeout: float = 3.0):
        return self.wait_for_payload(mycroft_msg_type, timeout=timeout,
                                     message_type=HiveMessageType.BUS)

    def wait_for_response(self, message: Union[MycroftMessage, HiveMessage],
                          reply_type: Optional[Union[HiveMessageType, str]] = None,
                          timeout=3.0):
        """Send a message and wait for a response.

        Arguments:
            message (HiveMessage): message to send, mycroft Message objects also accepted
            reply_type (HiveMessageType): the message type of the expected reply.
                                          Defaults to "<message.msg_type>".
            timeout: seconds to wait before timeout, defaults to 3

        Returns:
            The received message or None if the response timed out
        """
        message_type = reply_type or message.msg_type
        if isinstance(message, MycroftMessage):
            waiter = HivePayloadWaiter(bus=self, payload_type=message_type)
        else:
            waiter = HiveMessageWaiter(bus=self, message_type=message_type)  # Setup response handler
        # Send message and wait for it's response
        self.emit(message)
        return waiter.wait(timeout)

    def wait_for_payload_response(self, message: Union[MycroftMessage, HiveMessage],
                                  payload_type: Union[HiveMessageType, str],
                                  reply_type: Optional[Union[HiveMessageType, str]] = None,
                                  timeout=3.0):
        """Send a message and wait for a response.

        Arguments:
            message (HiveMessage): message to send, mycroft Message objects also accepted
            payload_type (str): the message type of the expected payload
            reply_type (HiveMessageType): the message type of the expected reply.
                                          Defaults to "<message.msg_type>".
            timeout: seconds to wait before timeout, defaults to 3

        Returns:
            The received message or None if the response timed out
        """
        if isinstance(message, MycroftMessage):
            message = HiveMessage(msg_type=HiveMessageType.BUS, payload=message)
        message_type = reply_type or message.msg_type
        waiter = HivePayloadWaiter(bus=self, payload_type=payload_type,
                                   message_type=message_type)  # Setup
        # response handler
        # Send message and wait for it's response
        self.emit(message)
        return waiter.wait(timeout)

    # targeted messages for nodes, asymmetric encryption
    def emit_intercom(self, message: Union[MycroftMessage, HiveMessage],
                      pubkey: Union[str, bytes, RSA.RsaKey]):

        encrypted_message = encrypt_RSA(pubkey, message.serialize())

        # sign message
        private_key = load_RSA_key(self.identity.private_key)
        signature = sign_RSA(private_key, encrypted_message)

        self.emit(HiveMessage(HiveMessageType.INTERCOM, payload={"ciphertext": pybase64.b64encode(encrypted_message),
                                                                 "signature": pybase64.b64encode(signature)}))

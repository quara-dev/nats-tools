import typing as t
from dataclasses import dataclass

from .tls import TLS


@dataclass
class MQTT:
    """"""

    listen: t.Optional[str] = None
    """Specify a host and port to listen for MQTT connections."""

    host: t.Optional[str] = None
    """MQTT server listening host."""

    port: t.Optional[int] = None
    """MQTT server listening port."""

    tls: t.Optional[TLS] = None
    """TLS configuration"""

    no_auth_user: t.Optional[str] = None
    """If no user name is provided when an MQTT client connects, will default this user name.
    Note that this is not compatible with running the server in operator mode.
    """

    ack_wait: t.Optional[str] = None
    """the amount of time after which a QoS 1 message sent to
    a client is redelivered as a DUPLICATE if the server has not
    received the PUBACK packet on the original Packet Identifier.
    The value has to be positive.
    Zero will cause the server to use the default value (30 seconds).
    Expressed as a time duration, with "s", "m", "h" indicating seconds,
    minutes and hours respectively. For instance "10s" for 10 seconds,
    "1m" for 1 minute, etc...
    """

    max_ack_pending: t.Optional[int] = None
    """amount of QoS 1 messages the server can send to
    a subscription without receiving any PUBACK for those messages.
    The valid range is [0..65535].
    """

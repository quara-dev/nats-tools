import typing as t
from dataclasses import dataclass

from .authorization import Authorization
from .tls import TLS


@dataclass
class LeafnodeUser:
    """Credentials and accounts to bind to leaf node connection.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/leafnodes/leafnode_conf#authorization-block
    """

    user: t.Optional[str] = None
    """Username for the leaf node connection."""

    password: t.Optional[str] = None
    """Password for the user entry."""

    account: t.Optional[str] = None
    """Account this leaf node connection should be bound to."""


@dataclass
class LeanodeAuthorization:
    """Leafnode Authorization

    Reference: https://docs.nats.io/running-a-nats-service/configuration/leafnodes/leafnode_conf#authorization-block
    """

    user: t.Optional[str] = None
    """Username for the leaf node connection."""

    password: t.Optional[str] = None
    """Password for the user entry."""

    account: t.Optional[str] = None
    """Account this leaf node connection should be bound to."""

    timeout: t.Optional[int] = None
    """Maximum number of seconds to wait for leaf node authentication."""

    users: t.Optional[t.List[LeafnodeUser]] = None
    """List of credentials and account to bind to leaf node connections."""


@dataclass
class RemoteLeafnode:
    """Leafnode remote configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/leafnodes/leafnode_conf#leafnode-remotes-entry-block
    """

    url: t.Optional[str] = None
    """Leafnode URL (URL protocol should be nats-leaf)."""

    urls: t.Optional[t.List[str]] = None
    """Leafnode URL array. Supports multiple URLs for discovery, e.g., urls: [ "nats-leaf://host1:7422", "nats-leaf://host2:7422" ]"""

    account: t.Optional[str] = None
    """Account name or JWT public key identifying the local account to bind to this remote server. Any traffic locally on this account will be forwarded to the remote server"""

    credentials: t.Optional[str] = None
    """Credential file for connecting to the leafnode server."""

    tls: t.Optional[TLS] = None
    """A TLS configuration block. Leafnode client will use specified TLS certificates when connecting/authenticating."""

    ws_compression: t.Optional[bool] = None
    """If connecting with Websocket protocol, this boolean (true or false) indicates to the remote server that it wishes to use compression. The default is false."""

    ws_no_masking: t.Optional[bool] = None
    """If connecting with Websocket protocol, this boolean indicates to the remote server that it wishes not to mask outbound WebSocket frames. The default is false, which means that outbound frames will be masked."""


@dataclass
class LeafNodes:
    """Leafnodes configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/leafnodes/leafnode_conf#leafnodes-configuration-block
    """

    host: t.Optional[str] = None
    """Interface where the server will listen for incoming leafnode connections."""

    port: t.Optional[int] = None
    """Port where the server will listen for incoming leafnode connections."""

    listen: t.Optional[str] = None
    """Listen specification `<host>:<port>` for leafnode connections. Either use this or the options host and/or port."""

    tls: t.Optional[TLS] = None
    """TLS configuration block (same as other nats-server tls configuration)."""

    advertise: t.Optional[str] = None
    """Hostport <host>:<port> to advertise how this server can be contacted by leaf nodes. This is useful in cluster setups with NAT"""

    no_advertise: t.Optional[bool] = None
    """if true the server shouldn't be advertised to leaf nodes."""

    authorization: t.Optional[Authorization] = None
    """Leafnode authorization configuration."""

    remotes: t.Optional[t.List[RemoteLeafnode]] = None
    """List of remote entries specifying servers where leafnode client connection can be made."""

    reconnect: t.Optional[int] = None
    """Interval in seconds at which reconnect attempts to a remote server are made."""

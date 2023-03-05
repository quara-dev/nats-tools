import typing as t
from dataclasses import dataclass

from .tls import TLS


@dataclass
class Websocket:
    """Enable websocket support.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/websocket/websocket_conf
    """

    listen: t.Optional[str] = None
    """Specify a host and port to listen for websocket connections."""

    host: t.Optional[str] = None
    """Websocket listening host."""

    port: t.Optional[int] = None
    """Websocket listening port."""

    advertise: t.Optional[str] = None
    """Specify what `<host>:<port>` to be advertised for websocket connections."""

    tls: t.Optional[TLS] = None
    """TLS Configuration is required by default. In order to disabled TLS, set `no_tls` to `true`."""

    no_tls: t.Optional[bool] = None
    """Disable need for TLS by explicitely settings `no_tls` to `true`."""

    same_origin: t.Optional[bool] = None
    """When set to `true`, the HTTP origin header must match the request’s hostname.
    This option is used only when the http request presents an Origin
    header, which is the case for web browsers. If no Origin header is present,
    this check will not be performed.
    """

    allowed_origins: t.Optional[t.List[str]] = None
    """List of accepted origins.
    When empty, and `same_origin` is `false`, clients from any origin are allowed to connect.
    """

    compression: t.Optional[bool] = None
    """enables support for compressed websocket frames in the server.
    For compression to be used, both server and client have to support it.
    """

    handshake_timeout: t.Optional[str] = None
    """total time allowed for the server to read the client request and write the response back
    to the client. This includes the time needed for the TLS handshake.
    """

    jwt_cookie: t.Optional[str] = None
    """Name for an HTTP cookie, that if present will be used as a client JWT.

    If the client specifies a JWT in the CONNECT protocol, this option is ignored.
    """

    no_auth_user: t.Optional[str] = None
    """If no user name is provided when a websocket client connects, will default
    this user name in the authentication phase.
    Note that this is not compatible with running the server in operator mode.
    """

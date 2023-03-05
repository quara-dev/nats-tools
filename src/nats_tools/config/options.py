import typing as t
from dataclasses import dataclass
from pathlib import Path

from .blocks import (
    MQTT,
    TLS,
    Account,
    Authorization,
    Cluster,
    JetStream,
    LeafNodes,
    NATSResolver,
    Websocket,
)


@dataclass
class ConnectivityOptions:
    """NATS Server Connectivity options.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#connectivity
    """

    host: t.Optional[str] = "0.0.0.0"
    """NATS Server listening host."""

    port: t.Optional[int] = 4222
    """NATS Server listening port."""

    listen: t.Optional[str] = None
    """Listen specification `<host>:<port>` for client connections. Either use this or the options host and/or port."""

    client_advertise: t.Optional[str] = None
    """Alternative client listen specification `<host>:<port>` or just `<host>` to advertise to clients and other server."""

    tls: t.Optional[TLS] = None
    """Require TLS for client connections."""


@dataclass
class TimeoutsOptions:
    """NATS Server Connection Timeouts.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#connection-timeouts.
    """

    ping_interval: t.Optional[str] = None
    """Duration at which pings are sent to clients, leaf nodes and routes.
    In the presence of client traffic, such as messages or client side pings, the server will not send pings.
    """

    ping_max: t.Optional[int] = None
    """After how many unanswered pings the server will allow before closing the connection."""

    write_deadline: t.Optional[str] = None
    """Maximum number of seconds the server will block when writing. Once this threshold is exceeded the connection will be closed. See slow consumer on how to deal with this on the client."""


@dataclass
class LimitsOptions:
    """NATS Server Limits.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#limits"""

    max_connections: t.Union[int, str, None] = None
    """Maximum number of active client connections. Default to `64K`."""

    max_control_line: t.Optional[str] = None
    """Maximum length of a protocol line (including combined length of subject and queue group).
    Increasing this value may require client changes to be used. Applies to all traffic. Default to `4KB`."""

    max_payload: t.Optional[str] = None
    """Maximum number of bytes in a message payload. Default to `1MB`"""

    max_pending: t.Optional[str] = None
    """Maximum number of bytes buffered for a connection Applies to client connections. Default to `64M`."""

    max_subscriptions: t.Optional[int] = None
    """Maximum numbers of subscriptions per client and leafnode accounts connection."""


@dataclass
class MonitoringOptions:
    """Monitoring & Tracing.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#monitoring-and-tracing
    """

    server_name: t.Optional[str] = None
    """Server name (default auto-generated).
    When JetStream is used, withing a domain, all server names need to be unique.
    """

    server_tags: t.Optional[t.Dict[str, str]] = None
    """Key value tags describing properties of the server.
    This will be exposed through `/varz` and can be used for system resource requests, such as placement of streams.
    Note that the keypair will be presented as strings separated by ':'.
    """

    trace: t.Optional[bool] = None
    """If `true` enable protocol trace log messages. Excludes the system account."""

    trace_verbose: t.Optional[bool] = None
    """If `true` enable protocol trace log messages. Includes the system account."""

    debug: t.Optional[bool] = None
    """If `true` enable debug log messages."""

    logtime: t.Optional[bool] = None
    """If `false`, log without timestamps."""

    log_file: t.Union[str, Path, None] = None
    """Log file name, relative to process working directory."""

    log_size_limit: t.Optional[int] = None
    """Size in bytes after the log file rolls over to a new one."""

    max_traced_msg_len: t.Optional[int] = None
    """Set a limit to the trace of the payload of a message."""

    syslog: t.Optional[bool] = None
    """Log to syslog."""

    remote_syslog: t.Optional[str] = None
    """Syslog server address."""

    http_port: t.Optional[int] = None
    """HTTP listening port for server monitoring."""

    http: t.Optional[str] = None
    """Listen specification `<host>:<port>` for server monitoring."""

    https_port: t.Optional[int] = None
    """https port for server monitoring. This is influenced by the tls property."""

    https: t.Optional[str] = None
    """Listen specification `<host>:<port>` for TLS server monitoring."""

    http_base_path: t.Optional[str] = None
    """Base path for monitoring endpoints."""

    system_account: t.Optional[str] = None
    """Name of the system account. Users of this account can subscribe to system events."""

    pid_file: t.Union[str, Path, None] = None
    """File containing PID, relative to process working directory.
    This can serve as input to nats-server --signal.
    """

    ports_file_dir: t.Union[str, Path, None] = None
    """Directory to write a file containing the servers open ports to, relative to process working directory."""

    connect_error_reports: t.Optional[int] = None
    """Number of attempts at which a repeated failed route, gateway or leaf node connection is reported.
    Connect attempts are made once every second. Errors are reported every hour by default.
    """

    reconnect_error_reports: t.Optional[int] = None
    """Number of failed attempt to reconnect a route, gateway or leaf node connection.
    Default is to report every attempt.
    """


@dataclass
class RuntimeOptions:
    """NATS Server Runtime configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#runtime-configuration
    """

    disable_sublist_cache: t.Optional[bool] = None
    """If true disable subscription caches for all accounts. This is saves resources in situations where different subjects are used all the time."""

    lame_duck_duration: t.Optional[str] = None
    """In lame duck mode the server rejects new clients and slowly closes client connections. After this duration is over the server shuts down. This value cannot be set lower than 30 seconds."""

    lame_duck_grace_period: t.Optional[str] = None
    """This is the duration the server waits, after entering lame duck mode, before starting to close client connections."""


@dataclass
class AuthorizationOptions:
    authorization: t.Optional[Authorization] = None
    """Configuration map for client authentication/authorization."""

    no_auth_user: t.Optional[str] = None
    """Username present in the authorization block or an account.
    A client connecting without any form of authentication will be associated with this user, its permissions and account.
    Note that this is not compatible with the operator mode.
    """


@dataclass
class DecentralizedAuthorizationOptions:
    accounts: t.Optional[t.Dict[str, Account]] = None
    """Configuration map for multi tenancy via accounts."""

    operator: t.Optional[str] = None
    """Operator JWT or path to an operator JWT."""

    resolver: t.Optional[NATSResolver] = None
    """Enable built-in NATS resolver."""

    resolver_preload: t.Optional[t.Dict[str, str]] = None
    """Map to preload account public keys and their corresponding JWT.
    Keys consist of `<account public nkey>`, value is the `<corresponding jwt>`.
    """


@dataclass
class ServerOptions(
    RuntimeOptions,
    LimitsOptions,
    TimeoutsOptions,
    AuthorizationOptions,
    DecentralizedAuthorizationOptions,
    MonitoringOptions,
    ConnectivityOptions,
):
    """NATS server options as a flat data structure."""

    jetstream: t.Optional[JetStream] = None
    """Enable and configure Jetstream."""

    leafnodes: t.Optional[LeafNodes] = None
    """Enable and configure leafnode support."""

    cluster: t.Optional[Cluster] = None
    """Enable and configure cluster support."""

    websocket: t.Optional[Websocket] = None
    """Enable and configure websocket support."""

    mqtt: t.Optional[MQTT] = None
    """Enable and configure MQTT support."""

import typing as t
from dataclasses import dataclass

from .authorization import Authorization
from .tls import TLS


@dataclass
class Cluster:
    """NATS cluster mode configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_config
    """

    host: t.Optional[str] = None
    """Interface where the gateway will listen for incoming route connections."""

    port: t.Optional[int] = None
    """Port where the gateway will listen for incoming route connections."""

    listen: t.Optional[str] = None
    """Combines host and port as `<host>:<port>`."""

    tls: t.Optional[TLS] = None
    """A tls configuration map for securing the clustering connection. verify is always enabled and cert_file is used for client and server."""

    name: t.Optional[str] = None
    """Name of the cluster."""

    advertise: t.Optional[str] = None
    """Hostport <host>:<port> to advertise how this server can be contacted by other cluster members."""

    no_advertise: t.Optional[bool] = None
    """When set to 'true', the server will not send or gossip its client URLs to other servers in the cluster and will not tell its client about the other servers' client URLs."""

    routes: t.Optional[t.List[str]] = None
    """A list of other servers (URLs) to cluster with. Self-routes are ignored. Should authentication via token or username/password be required, specify them as part of the URL."""

    connect_retries: t.Optional[int] = None
    """After how many failed connect attempts to give up establishing a connection to a discovered route. Default is 0, do not retry. When enabled, attempts will be made once a second. This, does not apply to explicitly configured routes."""

    authorization: t.Optional[Authorization] = None
    """Authorization map for configuring cluster routes.
    When a single username/password is used, it defines the authentication mechanism this server expects,
    and how this server will authenticate itself when establishing a connection to a discovered route.
    This will not be used for routes explicitly listed in routes and therefore have to be provided as
    part of the URL."""

import typing as t
from dataclasses import dataclass


@dataclass
class NATSResolver:
    """Full NATS resolver.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/jwt/resolver#full
    """

    type: t.Literal["full", "cache"] = "full"
    """Resolver type: `full` or `cache`."""

    dir: str = "./jwt"
    """Directory in which the account jwts will be stored."""

    allow_delete: bool = False
    """When `true`, support JWT deletion."""

    interval: str = "2m"
    """Interval at which a nats-server with a nats based account resolver will compare
    it's state with one random nats based account resolver in the cluster and if needed
    exchange jwt and converge on the same set of jwt.
    """

    limit: t.Optional[int] = None
    """Number of JWT to keep.

    For full resolvers, new JWT will be rejected once limit is reached.
    For cache resolvers, old JWT are evicted on new JWT.
    """

    ttl: t.Optional[str] = None
    """How long to hold on to a jwt before discarding it. """

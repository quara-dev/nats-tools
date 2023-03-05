import typing as t
from dataclasses import dataclass

from .users import User


@dataclass
class Authorization:
    """Client Authentication/Authorization

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro#authorization-map
    """

    user: t.Optional[str] = None
    """Specifies a single global user name for clients to the server (exclusive of token)"""

    password: t.Optional[str] = None
    """Specifies a single global password for clients to the server (exclusive of token)."""

    token: t.Optional[str] = None
    """Specifies a global token that can be used to authenticate to the server (exclusive of user and password)"""

    users: t.Optional[t.List[User]] = None
    """A list of user configuration maps. For multiple username and password credentials, specify a users list."""

import typing as t
from dataclasses import dataclass


@dataclass
class Permission:
    """Explicitely list subject to allow or deny.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/authorization#permission-map
    """

    allow: t.Optional[t.List[str]] = None
    deny: t.Optional[t.List[str]] = None


@dataclass
class AllowResponses:
    """Dynamically allows publishing to reply subjects.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/authorization#allow-responses-map
    """

    max: t.Optional[int] = None
    expires: t.Optional[str] = None


@dataclass
class Permissions:
    """The user permissions map specify subjects that can be subscribed to or published by the specified client.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/authorization#permissions-configuration-map
    """

    publish: t.Union[str, t.List[str], Permission, None] = None
    """subject, list of subjects, or permission map the client can publish"""

    subscribe: t.Union[str, t.List[str], Permission, None] = None
    """subject, list of subjects, or permission map the client can subscribe to."""

    allow_responses: t.Union[bool, AllowResponses, None] = None
    """boolean or responses map, default is false.
    Enabling this implicitly denies publish to other subjects, however an explicit publish
    allow on a subject will override this implicit deny for that subject.
    """


@dataclass
class User:
    """Specifies credentials and permissions options for a single user.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro#user-configuration-map
    """

    user: str  # NOSONAR
    """username for client authentication. (Can also be a user for tls authentication)."""

    password: str
    """password for the user entry."""

    nkey: t.Optional[str] = None
    """public nkey identifying an user."""

    permissions: t.Optional[Permissions] = None
    """Permissions map configuring subjects accessible to the user."""

    allowed_connection_types: t.Optional[
        t.List[t.Literal["STANDARD", "WEBSOCKET", "MQTT", "LEAFNODE"]]
    ] = None
    """Restrict which type of connections are allowed for a specific user."""

import typing as t
from dataclasses import dataclass

from .users import User


@dataclass
class StreamExport:
    """Bind a subject for use as a stream from other accounts.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts#export-configuration-map
    """

    stream: str
    """A subject or subject with wildcards that the account will publish."""

    accounts: t.Optional[t.List[str]] = None
    """A list of account names that can import the stream. If not specified, the stream is public and any account can import it."""


@dataclass
class ServiceExport:
    """Bind a subject for use as a service from other accounts.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts#export-configuration-map
    """

    service: str
    """A subject or subject with wildcards that the account will subscribe to."""

    accounts: t.Optional[t.List[str]] = None
    """A list of account names that can import the service. If not specified, the service is public and any account can import it."""

    response_type: t.Optional[str] = None
    """Indicates if a response to a service request consists of a single or a stream of messages.
    Possible values are: single or stream. (Default value is singleton)
    """


@dataclass
class Source:
    """Source configuration map.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts#source-configuration-map
    """

    account: str
    """Account name owning the export."""

    subject: str
    """The subject under which the stream or service is made accessible to the importing account"""


@dataclass
class StreamImport:
    """Enables account to consume a stream published by another account.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts#import-configuration-map
    """

    stream: Source
    """Stream import source configuration."""

    prefix: t.Optional[str] = None
    """A local subject prefix mapping for the imported stream."""


@dataclass
class ServiceImport:
    """Enables account to consume a service implemented by another account.

    References: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts#import-configuration-map
    """

    service: Source
    """Service import source configuration."""

    to: t.Optional[str] = None
    """A local subject mapping for imported service."""


@dataclass
class AccountJetStreamLimits:
    """JetStream account limits.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/resource_management#setting-account-resource-limits.
    """

    max_mem: t.Union[str, int, None] = None
    """Maximum size of the `memory` storage. Default unit is bytes when integer is provided."""

    max_file: t.Union[str, int, None] = None
    """Maximum size of the `file` storage. Default unit is bytes when integer is provided."""

    max_streams: t.Optional[int] = None
    """Maximum number of streams."""

    max_consumers: t.Optional[int] = None
    """Maximum number of consumers."""


@dataclass
class Account:
    """Multi-tenance account configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts
    """

    users: t.List[User]
    """Users which can connect to the account using username/password auth."""

    exports: t.Optional[t.Sequence[t.Union[ServiceExport, StreamExport]]] = None
    """Define account exports."""

    imports: t.Optional[t.Sequence[t.Union[StreamImport, ServiceImport]]] = None
    """Define account imports."""

    jetstream: t.Optional[AccountJetStreamLimits] = None
    """Resource limits for the account."""

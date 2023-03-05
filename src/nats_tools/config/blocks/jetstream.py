import typing as t
from dataclasses import dataclass


@dataclass
class JetStream:
    """Enable and configure JetStream.

    Reference: https://docs.nats.io/running-a-nats-service/configuration#jetstream
    """

    store_dir: t.Optional[str] = None
    """Directory to use for JetStream storage.
    Default to `/tmp/nats/jetstream`."""

    max_mem: t.Union[str, int, None] = None
    """Maximum size of the `memory` storage. Default to `75%` of available memory."""

    max_file: t.Union[str, int, None] = None
    """Maximum size of the `file` storage. Up to `1TB` if available."""

    cipher: t.Optional[str] = None
    """Set to enable storage-level encryption at rest. Choose either `chachapoly` or `aes`"""

    key: t.Optional[str] = None
    """The encryption key to use when encryption is enabled. A key length of at least 32 bytes is recommended. Note, this key is HMAC-256 hashed on startup which reduces the byte length to 64."""

    max_outstanding_catchup: t.Optional[str] = None
    """Max in-flight bytes for stream catch-up. Default to `32MB`."""

    domain: t.Optional[str] = None
    """Jetstream domain."""

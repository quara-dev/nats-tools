import typing as t
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TLS:
    """TLS Configuration.

    Reference: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/tls
    """

    cert_file: t.Union[str, Path, None] = None
    """TLS certificate file."""

    key_file: t.Union[str, Path, None] = None
    """TLS certificate key file."""

    ca_file: t.Union[str, Path, None] = None
    """TLS certificate authority file. When not present, default to the system trust store."""

    cipher_suites: t.Optional[t.List[str]] = None
    """When set, only the specified TLS cipher suites will be allowed. Values must match the golang version used to build the server."""

    curve_preferences: t.Optional[t.List[str]] = None
    """List of TLS cipher curves to use in order."""

    insecure: t.Optional[bool] = None
    """Skip certificate verification. This only applies to outgoing connections, NOT incoming client connections. NOT Recommended."""

    timeout: t.Optional[float] = None
    """TLS handshake timeout in fractional seconds. Default set to 0.5 seconds."""

    verify: t.Optional[bool] = None
    """If true, require and verify client certificates. To support use by Browser, this option does not apply to monitoring."""

    verify_and_map: t.Optional[bool] = None
    """If true, require and verify client certificates and map certificate values for authentication purposes. Does not apply to monitoring either."""

    verify_cert_and_check_known_urls: t.Optional[bool] = None
    """Only settable in a non client context where verify: true is the default (cluster/gateway).
    The incoming connections certificate's X509v3 Subject Alternative Name DNS entries will be matched against all urls in the configuration context that contains this tls map.
    If a match is found, the connection is accepted and rejected otherwise.
    """

    pinned_certs: t.Optional[t.List[str]] = None
    """List of hex-encoded SHA256 of DER encoded public key fingerprints.
    When present, during the TLS handshake, the provided certificate's fingerprint is required to be present in the list or the connection is closed.
    """

from dataclasses import dataclass


@dataclass
class TLSCertificates:
    ca_file: str
    cert_file: str
    key_file: str
    client_cert_file: str
    client_key_file: str

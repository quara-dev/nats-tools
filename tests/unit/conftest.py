import shutil
import tempfile
import typing as t
from pathlib import Path

import pytest
import trustme

from .entitites import TLSCertificates


@pytest.fixture
def tls_files() -> t.Iterator[TLSCertificates]:
    x509_ca = trustme.CA(organization_unit_name="nats-tools")
    x509_server_cert = x509_ca.issue_server_cert("server")
    x509_client_cert = x509_ca.issue_cert("client")
    tmpdir = Path(tempfile.mkdtemp(prefix="nats_tools_tls_", suffix="-"))
    # Initialize certificates paths
    ca_cert = tmpdir / "ca.crt"
    ca_cert.write_bytes(x509_ca.cert_pem.bytes())
    ca_key = tmpdir / "ca.key"
    ca_key.write_bytes(x509_ca.private_key_pem.bytes())
    server_cert = tmpdir / "server.crt"
    server_cert.write_bytes(x509_server_cert.private_key_and_cert_chain_pem.bytes())
    server_key = tmpdir / "server.key"
    server_key.write_bytes(x509_server_cert.private_key_and_cert_chain_pem.bytes())
    client_cert = tmpdir / "client.crt"
    client_cert.write_bytes(x509_client_cert.private_key_and_cert_chain_pem.bytes())
    client_key = tmpdir / "client.key"
    client_key.write_bytes(x509_client_cert.private_key_and_cert_chain_pem.bytes())
    try:
        yield TLSCertificates(
            ca_file=ca_cert.as_posix(),
            key_file=server_key.as_posix(),
            cert_file=server_cert.as_posix(),
            client_cert_file=client_cert.as_posix(),
            client_key_file=client_key.as_posix(),
        )
    finally:
        shutil.rmtree(tmpdir)

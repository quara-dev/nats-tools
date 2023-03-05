from nats_tools.config import ServerOptions, non_null, render
from nats_tools.config.blocks import (
    MQTT,
    TLS,
    Account,
    AccountJetStreamLimits,
    Authorization,
    Cluster,
    JetStream,
    LeafNodes,
    NATSResolver,
    Permissions,
    RemoteLeafnode,
    ServiceExport,
    ServiceImport,
    Source,
    StreamExport,
    StreamImport,
    User,
    Websocket,
)

from .entitites import TLSCertificates


def test_config_with_default_values() -> None:
    """Test that config can be generated with default values only."""
    options = ServerOptions()
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
"""
    )


def test_config_with_listen_address() -> None:
    """Test that config can be generated with listen address."""
    address = "127.0.0.1:4222"
    options = ServerOptions(listen=address)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "listen": address}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening address
listen: {address}
"""
    )


def test_config_with_client_advertise() -> None:
    """Test that config can be generated with client_advertise."""
    advertise_address = "somewhere:8888"
    options = ServerOptions(client_advertise=advertise_address)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "client_advertise": advertise_address,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Address advertised to client
client_advertise: {advertise_address}
"""
    )


def test_config_with_tls(tls_files: TLSCertificates) -> None:
    options = ServerOptions(
        tls=TLS(
            cert_file=tls_files.cert_file,
            key_file=tls_files.key_file,
            ca_file=tls_files.ca_file,
        )
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "tls": {
            "cert_file": tls_files.cert_file,
            "key_file": tls_files.key_file,
            "ca_file": tls_files.ca_file,
        },
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Configure TLS for client connections
tls: {{
  "ca_file": "{tls_files.ca_file}",
  "cert_file": "{tls_files.cert_file}",
  "key_file": "{tls_files.key_file}"
}}
"""
    )


def test_config_with_ping_interval() -> None:
    """Test that config can be generated with ping interval."""
    ping_interval = "2s"
    options = ServerOptions(ping_interval=ping_interval)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "ping_interval": ping_interval,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Duration at which pings are sent to clients, leaf nodes and routes
ping_interval: {ping_interval}
"""
    )


def test_config_with_ping_max() -> None:
    """Test that config can be generated with ping max."""
    ping_max = 1
    options = ServerOptions(ping_max=ping_max)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "ping_max": ping_max}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# After how many unanswered pings the server will allow before closing the connection
ping_max: {ping_max}
"""
    )


def test_config_with_write_deadline() -> None:
    """Test that config can be generated with custom write_deadline"""
    write_deadline = "1s"
    options = ServerOptions(write_deadline=write_deadline)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "write_deadline": write_deadline,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum number of seconds the server will block when writing. Once this threshold is exceeded the connection will be closed
write_deadline: "{write_deadline}"
"""
    )


def test_config_with_max_connections() -> None:
    max_connections = 1
    options = ServerOptions(max_connections=max_connections)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_connections": max_connections,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum number of active client connections
max_connections: {max_connections}
"""
    )


def test_config_with_max_control_line() -> None:
    max_control_line = "2KB"
    options = ServerOptions(max_control_line=max_control_line)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_control_line": max_control_line,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum length of a protocol line (including combined length of subject and queue group)
max_control_line: {max_control_line}
"""
    )


def test_config_with_max_payload() -> None:
    max_payload = "2KB"
    options = ServerOptions(max_payload=max_payload)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_payload": max_payload,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum number of bytes in a message payload
max_payload: {max_payload}
"""
    )


def test_config_with_max_pending() -> None:
    max_pending = "2MB"
    options = ServerOptions(max_pending=max_pending)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_pending": max_pending,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum number of bytes in a message payload
max_pending: {max_pending}
"""
    )


def test_config_with_max_subscriptions() -> None:
    max_subscriptions = 1000
    options = ServerOptions(max_subscriptions=max_subscriptions)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_subscriptions": max_subscriptions,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Maximum numbers of subscriptions per client and leafnode accounts connection
max_subscriptions: {max_subscriptions}
"""
    )


def test_config_with_server_name() -> None:
    server_name = "test"
    options = ServerOptions(server_name=server_name)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "server_name": server_name,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# NATS server name
server_name: {server_name}
"""
    )


def test_config_with_server_tags() -> None:
    server_tags = {"environment": "test", "project": "nats-tools"}
    options = ServerOptions(server_tags=server_tags)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "server_tags": server_tags,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Key value tags describing properties of the server
# Tags will be exposed through `/varz` and can be used
# for system resource requests, such as placement of streams
server_tags: [
  "environment:{server_tags['environment']}",
  "project:{server_tags['project']}"
]
"""
    )


def test_config_with_trace() -> None:
    options = ServerOptions(trace=True)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "trace": True}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable protocol trace log messages (excluding the system account)
trace: true
"""
    )


def test_config_with_trace_verbose() -> None:
    options = ServerOptions(trace_verbose=True)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "trace_verbose": True}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable protocol trace log messages (including the system account)
trace_verbose: true
"""
    )


def test_config_with_debug() -> None:
    options = ServerOptions(debug=True)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "debug": True}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable debug log messages
debug: true
"""
    )


def test_config_with_logtime() -> None:
    options = ServerOptions(logtime=False)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "logtime": False}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Log without timestamp
logtime: false
"""
    )


def test_config_with_log_file() -> None:
    log_file = "test.log"
    options = ServerOptions(log_file=log_file)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "log_file": log_file}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Write logs to file
log_file: {log_file}
"""
    )


def test_config_with_log_file_size_limit() -> None:
    log_size_limit = 2048
    options = ServerOptions(log_size_limit=log_size_limit)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "log_size_limit": log_size_limit,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Roll over to a new file after limit is reached
log_size_limit: {log_size_limit}
"""
    )


def test_config_with_max_traced_msg_len() -> None:
    max_traced_msg_len = 2048
    options = ServerOptions(max_traced_msg_len=max_traced_msg_len)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "max_traced_msg_len": max_traced_msg_len,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Set a limit to the trace of the payload of a message
max_traced_msg_len: {max_traced_msg_len}
"""
    )


def test_config_with_syslog() -> None:
    options = ServerOptions(syslog=True)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "syslog": True}
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Log to syslog
syslog: true
"""
    )


def test_config_with_remote_syslog() -> None:
    remote_syslog = "some-remote:9000"
    options = ServerOptions(remote_syslog=remote_syslog)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "remote_syslog": remote_syslog,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Log to remote syslog
remote_syslog: {remote_syslog}
"""
    )


def test_config_with_http_port() -> None:
    http_port = 9000
    options = ServerOptions(http_port=http_port)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "http_port": http_port,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable monitoring endpoint
http_port: {http_port}
"""
    )


def test_config_with_http_address() -> None:
    address = "0.0.0.0:8000"
    options = ServerOptions(http=address)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "http": address}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable monitoring endpoint
http: {address}
"""
    )


def test_config_with_https_port() -> None:
    https_port = 9000
    options = ServerOptions(https_port=https_port)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "https_port": https_port,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable monitoring endpoint with TLS
https_port: {https_port}
"""
    )


def test_config_with_https_address() -> None:
    address = "0.0.0.0:8000"
    options = ServerOptions(https=address)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "https": address}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable monitoring endpoint with TLS
https: {address}
"""
    )


def test_config_with_system_account() -> None:
    account_name = user_name = password = "test"
    accounts = {account_name: Account(users=[User(user=user_name, password=password)])}
    options = ServerOptions(system_account=account_name, accounts=accounts)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "system_account": account_name,
        "accounts": non_null(accounts),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Configure system account
system_account: {account_name}
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "users": [
      {{
        "password": "{password}",
        "user": "{user_name}"
      }}
    ]
  }}
}}
"""
    )


def test_config_with_pid_file() -> None:
    pid_file = "test.pid"
    options = ServerOptions(pid_file=pid_file)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "pid_file": pid_file}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Write process PID to file
pid_file: {pid_file}
"""
    )


def test_config_with_ports_file_dir() -> None:
    ports_file_dir = "ports/"
    options = ServerOptions(ports_file_dir=ports_file_dir)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "ports_file_dir": ports_file_dir,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Write process PID to file within directory
# File will be named "nats-server_<pid>.ports"
# Directory MUST exist before starting nats-server
ports_file_dir: {ports_file_dir}
"""
    )


def test_config_with_connect_error_reports() -> None:
    connect_error_reports = 1
    options = ServerOptions(connect_error_reports=connect_error_reports)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "connect_error_reports": connect_error_reports,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Number of attempts at which a repeated failed route, gateway or leaf node connection is reported
connect_error_reports: {connect_error_reports}
"""
    )


def test_config_with_reconnect_error_reports() -> None:
    reconnect_error_reports = 1
    options = ServerOptions(reconnect_error_reports=reconnect_error_reports)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "reconnect_error_reports": reconnect_error_reports,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Number of attempts at which a repeated failed route, gateway or leaf node reconnect is reported
reconnect_error_reports: {reconnect_error_reports}
"""
    )


def test_config_with_disable_sublist_cache() -> None:
    options = ServerOptions(disable_sublist_cache=True)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "disable_sublist_cache": True,
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Disable subscription caches for all accounts
# This is saves resources in situations where different subjects are used all the time
disable_sublist_cache: true
"""
    )


def test_config_with_lame_duck_duration() -> None:
    lame_duck_duration = "30s"
    options = ServerOptions(lame_duck_duration=lame_duck_duration)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "lame_duck_duration": lame_duck_duration,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# In lame duck mode the server rejects new clients and slowly closes client connections
# After this duration is over the server shuts down
# Note that this value cannot be set lower than 30 seconds
lame_duck_duration: "{lame_duck_duration}"
"""
    )


def test_config_with_duck_grace_period() -> None:
    lame_duck_grace_period = "5s"
    options = ServerOptions(lame_duck_grace_period=lame_duck_grace_period)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "lame_duck_grace_period": lame_duck_grace_period,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# The duration the server waits (after entering lame duck mode)
# before starting to close client connections
lame_duck_grace_period: "{lame_duck_grace_period}"
"""
    )


def test_config_with_user_password_authorization() -> None:
    authorization = Authorization(user="test", password="test")
    options = ServerOptions(authorization=authorization)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "authorization": non_null(authorization),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Configuration map for client authentication/authorization
authorization: {{
  "password": "{authorization.password}",
  "user": "{authorization.user}"
}}
"""
    )


def test_config_with_multi_users() -> None:
    user1 = password1 = "test"
    user2 = password2 = "other"
    user3 = password3 = "yetanother"
    authorization = Authorization(
        users=[
            User(user=user1, password=password1),
            User(
                user=user2,
                password=password2,
                allowed_connection_types=["STANDARD", "WEBSOCKET"],
            ),
            User(
                user=user3,
                password=password3,
                permissions=Permissions(publish=["test.*"]),
            ),
        ]
    )
    options = ServerOptions(authorization=authorization)
    assert non_null(authorization) == {
        "users": [
            {"user": user1, "password": password1},
            {
                "user": user2,
                "password": password2,
                "allowed_connection_types": ["STANDARD", "WEBSOCKET"],
            },
            {
                "user": user3,
                "password": password3,
                "permissions": {"publish": ["test.*"]},
            },
        ]
    }
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "authorization": non_null(authorization),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Configuration map for client authentication/authorization
authorization: {{
  "users": [
    {{
      "password": "{password1}",
      "user": "{user1}"
    }},
    {{
      "allowed_connection_types": [
        "STANDARD",
        "WEBSOCKET"
      ],
      "password": "{password2}",
      "user": "{user2}"
    }},
    {{
      "password": "{password3}",
      "permissions": {{
        "publish": [
          "test.*"
        ]
      }},
      "user": "{user3}"
    }}
  ]
}}
"""
    )


def test_config_with_token_authorization() -> None:
    authorization = Authorization(token="test")
    options = ServerOptions(authorization=authorization)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "authorization": non_null(authorization),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Configuration map for client authentication/authorization
authorization: {{
  "token": "{authorization.token}"
}}
"""
    )


def test_config_with_accounts_and_no_auth_user() -> None:
    account_name = user = password = no_auth_user = "test"
    accounts = {account_name: Account(users=[User(user=user, password=password)])}
    options = ServerOptions(accounts=accounts, no_auth_user=no_auth_user)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
        "no_auth_user": no_auth_user,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# A client connecting without any form of authentication will be associated with this user, its permissions and account
no_auth_user: "{user}"
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }}
}}
"""
    )


def test_config_with_accounts_and_jetstream_limit() -> None:
    account_name = user = password = "test"
    limits = AccountJetStreamLimits(max_mem=10, max_file=20)
    accounts = {
        account_name: Account(
            users=[User(user=user, password=password)], jetstream=limits
        )
    }
    options = ServerOptions(accounts=accounts)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "jetstream": {{
      "max_file": {limits.max_file},
      "max_mem": {limits.max_mem}
    }},
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }}
}}
"""
    )


def test_config_with_accounts_and_exports() -> None:
    account_name = user = password = "test"
    stream_subject = "test-stream"
    service_subject = "test-service"
    accounts = {
        account_name: Account(
            users=[User(user=user, password=password)],
            exports=[
                StreamExport(stream=stream_subject),
                ServiceExport(service=service_subject),
            ],
        )
    }
    options = ServerOptions(accounts=accounts)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "exports": [
      {{
        "stream": "{stream_subject}"
      }},
      {{
        "service": "{service_subject}"
      }}
    ],
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }}
}}
"""
    )


def test_config_with_accounts_and_imports() -> None:
    account_name = user = password = "test"
    account_name2 = user2 = password2 = "test2"
    stream_subject = "test-stream"
    service_subject = "test-service"
    accounts = {
        account_name: Account(
            users=[User(user=user, password=password)],
            exports=[
                StreamExport(stream=stream_subject),
                ServiceExport(service=service_subject),
            ],
        ),
        account_name2: Account(
            users=[User(user=user2, password=password2)],
            imports=[
                StreamImport(
                    stream=Source(account=account_name, subject=stream_subject)
                ),
                ServiceImport(
                    service=Source(account=account_name, subject=service_subject)
                ),
            ],
        ),
    }
    options = ServerOptions(accounts=accounts)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "exports": [
      {{
        "stream": "{stream_subject}"
      }},
      {{
        "service": "{service_subject}"
      }}
    ],
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }},
  "{account_name2}": {{
    "imports": [
      {{
        "stream": {{
          "account": "{account_name}",
          "subject": "{stream_subject}"
        }}
      }},
      {{
        "service": {{
          "account": "{account_name}",
          "subject": "{service_subject}"
        }}
      }}
    ],
    "users": [
      {{
        "password": "{password2}",
        "user": "{user2}"
      }}
    ]
  }}
}}
"""
    )


def test_config_with_operator() -> None:
    operator = "eyJ0eXAiOiJKV1QiLCJhbGciOiJlZDI1NTE5LW5rZXkifQ.eyJqdGkiOiI2RVc0NEtIUlZRU1laN1lIWEpORVJCNzNLR1NKR1pPRVZRN0VTQUVWTkFaNFpGNVFEM1BBIiwiaWF0IjoxNjYzNzIwNjUyLCJpc3MiOiJPREc0WUpYTkhaSElDU0VPVVNLVlA1RFdWREZZR0pXNzRKTTVYRkxGSEZYS0tPRTVVQVNHUlRWNSIsIm5hbWUiOiJRVUFSQSIsInN1YiI6Ik9ERzRZSlhOSFpISUNTRU9VU0tWUDVEV1ZERllHSlc3NEpNNVhGTEZIRlhLS09FNVVBU0dSVFY1IiwibmF0cyI6eyJvcGVyYXRvcl9zZXJ2aWNlX3VybHMiOlsibmF0czovL2xvY2FsaG9zdDo0MjIyIl0sInN5c3RlbV9hY2NvdW50IjoiQURRRE5WS1hKVEZJRTNZTjRCQ0RHNVFLRlBJWlQ2TFFGVEhVV0taMkpZM04yRUVEUzUzMkdMSlciLCJ0eXBlIjoib3BlcmF0b3IiLCJ2ZXJzaW9uIjoyfX0.x2tWeEP5ofk3hpaWjRf_qlorB9XBzZMEoVCQnGB_nOiGxc65cGo98V-TRLmofvE4miwhbDAdBj9fh-jeuyjMBA"
    options = ServerOptions(operator=operator)
    assert non_null(options) == {"host": "0.0.0.0", "port": 4222, "operator": operator}
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable operator authorization mode
operator: {operator}
"""
    )


def test_config_with_resolver() -> None:
    resolver = NATSResolver()
    options = ServerOptions(resolver=resolver)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "resolver": non_null(resolver),
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Use NATS resolver to resolve accounts
resolver: {{
  "allow_delete": {'true' if resolver.allow_delete else 'false'},
  "dir": "{resolver.dir}",
  "interval": "{resolver.interval}",
  "type": "{resolver.type}"
}}
"""
    )


def test_config_with_resolver_preload() -> None:
    resolver_preload = {
        "ACP5QLX7CZ7345FB4A3XHCZNFEUV4NHZ2HL743IXZVD7FCKWLX2BDVZY": "eyJ0eXAiOiJKV1QiLCJhbGciOiJlZDI1NTE5LW5rZXkifQ.eyJqdGkiOiJIVTJHS0tVM0hNQlhXUVhDWllHWlVFNjdRTkVNQUdJT1o3NUVFVkJaNDNZNE5OV0g0UERRIiwiaWF0IjoxNjYzNzIwNjUyLCJpc3MiOiJPREc0WUpYTkhaSElDU0VPVVNLVlA1RFdWREZZR0pXNzRKTTVYRkxGSEZYS0tPRTVVQVNHUlRWNSIsIm5hbWUiOiJRVUFSQSIsInN1YiI6IkFDUDVRTFg3Q1o3MzQ1RkI0QTNYSENaTkZFVVY0TkhaMkhMNzQzSVhaVkQ3RkNLV0xYMkJEVlpZIiwibmF0cyI6eyJsaW1pdHMiOnsic3VicyI6LTEsImRhdGEiOi0xLCJwYXlsb2FkIjotMSwiaW1wb3J0cyI6LTEsImV4cG9ydHMiOi0xLCJ3aWxkY2FyZHMiOnRydWUsImNvbm4iOi0xLCJsZWFmIjotMX0sImRlZmF1bHRfcGVybWlzc2lvbnMiOnsicHViIjp7fSwic3ViIjp7fX0sInR5cGUiOiJhY2NvdW50IiwidmVyc2lvbiI6Mn19.Bw-PfEAy9g3eE1UZDFXqA4xM9_nQtp26bZWKw0nynDduZS5zbOfm6tgz8fxjvyB13yyIoXQzKRqqPL8Ea2ejBA"
    }

    options = ServerOptions(resolver_preload=resolver_preload)
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "resolver_preload": resolver_preload,
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Accounts JWT allowed to connect to the server by default
# Once server is started, accounts can be managed using NATS resolver
# Note that only system account is allowed to communicate with NATS resolver
resolver_preload: {{
  "{list(resolver_preload.keys())[0]}": "{list(resolver_preload.values())[0]}"
}}
"""
    )


def test_config_with_jetstream_default_values() -> None:
    options = ServerOptions(jetstream=JetStream())
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {}
"""
    )


def test_config_with_jetstream_store_dir() -> None:
    store_dir = "test"
    options = ServerOptions(jetstream=JetStream(store_dir=store_dir))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"store_dir": store_dir},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "store_dir": "{store_dir}"
}}
"""
    )


def test_config_with_jetstream_max_memory_store() -> None:
    max_mem = "2M"
    options = ServerOptions(jetstream=JetStream(max_mem=max_mem))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"max_mem": max_mem},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "max_mem": "{max_mem}"
}}
"""
    )


def test_config_with_jetstream_max_file() -> None:
    max_file = "2M"
    options = ServerOptions(jetstream=JetStream(max_file=max_file))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"max_file": max_file},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "max_file": "{max_file}"
}}
"""
    )


def test_config_with_jetstream_encryption_cipher_and_key() -> None:
    cipher = "chachapoly"
    key = "6dYfBV0zzEkR3vxZCNjxmnVh/aIqgid1"
    options = ServerOptions(jetstream=JetStream(cipher=cipher, key=key))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"cipher": cipher, "key": key},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "cipher": "{cipher}",
  "key": "{key}"
}}
"""
    )


def test_config_with_jetstream_max_outstanding_catchup() -> None:
    max_outstanding_catchup = "2M"
    options = ServerOptions(
        jetstream=JetStream(max_outstanding_catchup=max_outstanding_catchup)
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"max_outstanding_catchup": max_outstanding_catchup},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "max_outstanding_catchup": "{max_outstanding_catchup}"
}}
"""
    )


def test_config_with_jetstream_domain() -> None:
    domain = "test"
    options = ServerOptions(jetstream=JetStream(domain=domain))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "jetstream": {"domain": domain},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable NATS JetStream
jetstream: {{
  "domain": "{domain}"
}}
"""
    )


def test_config_with_leafnodes_default_values() -> None:
    options = ServerOptions(leafnodes=LeafNodes(port=7422))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"port": 7422},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {
  # Listen for incoming leafnode connections
  port: 7422
}
"""
    )


def test_config_with_leafnodes_with_host() -> None:
    host = "0.0.0.0"
    options = ServerOptions(leafnodes=LeafNodes(port=7422, host=host))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"host": host, "port": 7422},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Listen for incoming leafnode connections
  host: {host}
  port: 7422
}}
"""
    )


def test_config_with_leafnodes_listen_address() -> None:
    address = "0.0.0.0:7422"
    options = ServerOptions(leafnodes=LeafNodes(listen=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"listen": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Listen for incoming leafnode connections
  listen: {address}
}}
"""
    )


def test_config_with_leafnodes_advertise() -> None:
    address = "somewhere:7422"
    options = ServerOptions(leafnodes=LeafNodes(port=7422, advertise=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"advertise": address, "port": 7422},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Listen for incoming leafnode connections
  port: 7422

  # Advertise how this server can be contacted by leaf nodes.
  advertise: {address}
}}
"""
    )


def test_config_with_leafnodes_no_advertise() -> None:
    options = ServerOptions(leafnodes=LeafNodes(port=7422, no_advertise=True))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"no_advertise": True, "port": 7422},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {
  # Listen for incoming leafnode connections
  port: 7422

  # Indicate that server shouldn't be advertised to leaf nodes.
  no_advertise: true
}
"""
    )


def test_config_with_leafnodes_remotes() -> None:
    remote_url = "nats-leaf://somewhere:4222"
    options = ServerOptions(
        leafnodes=LeafNodes(remotes=[RemoteLeafnode(url=remote_url)])
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"remotes": [{"url": remote_url}]},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Connect to remote leaf nodes
  remotes: [
    {{
      "url": "{remote_url}"
    }}
  ]
}}
"""
    )


def test_config_with_leafnodes_reconnect() -> None:
    reconnect = 5
    options = ServerOptions(leafnodes=LeafNodes(reconnect=5))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {"reconnect": reconnect},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Interval in seconds at which reconnect attempts to a remote server are made
  reconnect: {reconnect}
}}
"""
    )


def test_config_with_leafnodes_tls(tls_files: TLSCertificates) -> None:
    options = ServerOptions(
        leafnodes=LeafNodes(
            tls=TLS(
                cert_file=tls_files.cert_file,
                key_file=tls_files.key_file,
                ca_file=tls_files.ca_file,
            )
        )
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "leafnodes": {
            "tls": {
                "cert_file": tls_files.cert_file,
                "key_file": tls_files.key_file,
                "ca_file": tls_files.ca_file,
            }
        },
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure inbound and outbound leafnodes connections
leafnodes: {{
  # Require leafnodes to connect using TLS
  tls: {{
    "ca_file": "{tls_files.ca_file}",
    "cert_file": "{tls_files.cert_file}",
    "key_file": "{tls_files.key_file}"
  }}
}}
"""
    )


# TODO: Test leafnodes with authorization


def test_config_with_cluster_name() -> None:
    cluster_name = "test"
    options = ServerOptions(cluster=Cluster(name=cluster_name))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"name": cluster_name},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  name: {cluster_name}
}}
"""
    )


def test_config_with_cluster_host() -> None:
    cluster_host = "0.0.0.0"
    options = ServerOptions(cluster=Cluster(host=cluster_host))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"host": cluster_host},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # Listen for incoming cluster connections
  host: {cluster_host}
}}
"""
    )


def test_config_with_cluster_port() -> None:
    cluster_port = 6222
    options = ServerOptions(cluster=Cluster(port=cluster_port))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"port": cluster_port},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # Listen for incoming cluster connections
  port: {cluster_port}
}}
"""
    )


def test_config_with_cluster_listen() -> None:
    address = "0.0.0.0:6222"
    options = ServerOptions(cluster=Cluster(listen=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"listen": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # Listen for incoming cluster connections
  listen: {address}
}}
"""
    )


def test_config_with_cluster_advertise() -> None:
    address = "0.0.0.0:6222"
    options = ServerOptions(cluster=Cluster(advertise=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"advertise": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # Hostport <host>:<port> to advertise how this server can be contacted by other cluster members
  advertise: {address}
}}
"""
    )


def test_config_with_cluster_no_advertise() -> None:
    options = ServerOptions(cluster=Cluster(no_advertise=True))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"no_advertise": True},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {
  # Do not send or gossip server client URLs to other servers in the cluster
  # Also prevent server telling its client about the other servers' client URLs
  no_advertise: true
}
"""
    )


def test_config_with_cluster_routes() -> None:
    routes = ["nats://somewhere-else:6222"]
    options = ServerOptions(cluster=Cluster(routes=routes))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"routes": routes},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # A list of other servers (URLs) to cluster with. Self-routes are ignored.
  # Should authentication via token or username/password be required, specify them as part of the URL
  routes: [
    "{routes[0]}"
  ]
}}
"""
    )


def test_config_with_cluster_connect_retries() -> None:
    connect_retries = 2
    options = ServerOptions(cluster=Cluster(connect_retries=connect_retries))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {"connect_retries": connect_retries},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # After how many failed connect attempts to give up establishing a connection to a discovered route. Default is 0, do not retry. When enabled, attempts will be made once a second.
  # This, does not apply to explicitly configured routes
  connect_retries: {connect_retries}
}}
"""
    )


def test_config_with_cluster_tls(tls_files: TLSCertificates) -> None:
    options = ServerOptions(
        cluster=Cluster(
            tls=TLS(
                cert_file=tls_files.cert_file,
                key_file=tls_files.key_file,
                ca_file=tls_files.ca_file,
            )
        )
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "cluster": {
            "tls": {
                "cert_file": tls_files.cert_file,
                "key_file": tls_files.key_file,
                "ca_file": tls_files.ca_file,
            }
        },
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure cluster mode
cluster: {{
  # Configure TLS for communications between cluster members
  tls: {{
    "ca_file": "{tls_files.ca_file}",
    "cert_file": "{tls_files.cert_file}",
    "key_file": "{tls_files.key_file}"
  }}
}}
"""
    )


# TODO: Test cluster with authorization


def test_config_with_websocket_no_tls() -> None:
    options = ServerOptions(websocket=Websocket(no_tls=True))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"no_tls": True},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {
  # Serve plain websocket instead of secured websockets
  # Use it only when NATS is served behind a reverse-proxy
  # or during development
  no_tls: true
}
"""
    )


def test_config_with_websocket_tls(tls_files: TLSCertificates) -> None:
    options = ServerOptions(
        websocket=Websocket(
            tls=TLS(
                cert_file=tls_files.cert_file,
                key_file=tls_files.key_file,
                ca_file=tls_files.ca_file,
            )
        )
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {
            "tls": {
                "cert_file": tls_files.cert_file,
                "key_file": tls_files.key_file,
                "ca_file": tls_files.ca_file,
            }
        },
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Configure TLS
  tls: {{
    "ca_file": "{tls_files.ca_file}",
    "cert_file": "{tls_files.cert_file}",
    "key_file": "{tls_files.key_file}"
  }}
}}
"""
    )


def test_config_with_websocket_host() -> None:
    websocket_host = "0.0.0.0"
    options = ServerOptions(websocket=Websocket(host=websocket_host))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"host": websocket_host},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Listen for incoming websocket connections
  host: {websocket_host}
}}
"""
    )


def test_config_with_websocket_port() -> None:
    websocket_port = 6222
    options = ServerOptions(websocket=Websocket(port=websocket_port))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"port": websocket_port},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Listen for incoming websocket connections
  port: {websocket_port}
}}
"""
    )


def test_config_with_websocket_listen() -> None:
    address = "0.0.0.0:6222"
    options = ServerOptions(websocket=Websocket(listen=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"listen": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Listen for incoming websocket connections
  listen: {address}
}}
"""
    )


def test_config_with_websocket_advertise() -> None:
    address = "0.0.0.0:6222"
    options = ServerOptions(websocket=Websocket(advertise=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"advertise": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Hostport <host>:<port> to  to be advertised for websocket connections
  advertise: {address}
}}
"""
    )


def test_config_with_websocket_same_origin() -> None:
    options = ServerOptions(websocket=Websocket(same_origin=True))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"same_origin": True},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {
  # HTTP origin header must match the request’s hostname
  # If no Origin header is present, this check will not be performed
  same_origin: true
}
"""
    )


def test_config_with_websocket_allowed_origins() -> None:
    origins = ["example.com"]
    options = ServerOptions(websocket=Websocket(allowed_origins=origins))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"allowed_origins": origins},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # HTTP origin header must match one of allowed origins
  # If no Origin header is present, this check will not be performed
  allowed_origins: [
    "{origins[0]}"
  ]
}}
"""
    )


def test_config_with_websocket_compression() -> None:
    options = ServerOptions(websocket=Websocket(compression=True))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"compression": True},
    }
    config = render(options)
    assert config == (
        """# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {
  # Enable support for compressed websocket frames in the server
  # Note: for compression to be used, both server and client have to support it
  compression: true
}
"""
    )


def test_config_with_websocket_handshake_timeout() -> None:
    timeout = "30s"
    options = ServerOptions(websocket=Websocket(handshake_timeout=timeout))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"handshake_timeout": timeout},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Total time allowed for the server to read the client request and write the response back
  # to the client.
  handshake_timeout: "{timeout}"
}}
"""
    )


def test_config_with_websocket_jwt_cookie() -> None:
    cookie_name = "test"
    options = ServerOptions(websocket=Websocket(jwt_cookie=cookie_name))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "websocket": {"jwt_cookie": cookie_name},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure websocket server
websocket: {{
  # Name for an HTTP cookie, that if present will be used as a client JWT
  # If the client specifies a JWT in the CONNECT protocol, this option is ignored
  jwt_cookie: "{cookie_name}"
}}
"""
    )


def test_config_with_websocket_and_no_auth_user() -> None:
    account_name = user = password = "test"
    accounts = {account_name: Account(users=[User(user=user, password=password)])}
    options = ServerOptions(accounts=accounts, websocket=Websocket(no_auth_user=user))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
        "websocket": {"no_auth_user": user},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }}
}}

# Configure websocket server
websocket: {{
  # A client connecting without any form of authentication will be associated with this user, its permissions and account
  no_auth_user: "{user}"
}}
"""
    )


def test_config_with_mqtt_host() -> None:
    mqtt_host = "0.0.0.0"
    options = ServerOptions(mqtt=MQTT(host=mqtt_host))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {"host": mqtt_host},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # Listen for incoming MQTT connections
  host: {mqtt_host}
}}
"""
    )


def test_config_with_mqtt_port() -> None:
    mqtt_port = 6222
    options = ServerOptions(mqtt=MQTT(port=mqtt_port))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {"port": mqtt_port},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # Listen for incoming MQTT connections
  port: {mqtt_port}
}}
"""
    )


def test_config_with_mqtt_listen() -> None:
    address = "0.0.0.0:6222"
    options = ServerOptions(mqtt=MQTT(listen=address))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {"listen": address},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # Listen for incoming MQTT connections
  listen: {address}
}}
"""
    )


def test_config_with_mqtt_ack_wait() -> None:
    ack_wait = "10s"
    options = ServerOptions(mqtt=MQTT(ack_wait=ack_wait))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {"ack_wait": ack_wait},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # The amount of time after which a QoS 1 message sent to
  # a client is redelivered as a DUPLICATE if the server has not
  # received the PUBACK packet on the original Packet Identifier
  ack_wait: "{ack_wait}"
}}
"""
    )


def test_config_with_mqtt_max_ack_pending() -> None:
    max_ack_pending = 10
    options = ServerOptions(mqtt=MQTT(max_ack_pending=max_ack_pending))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {"max_ack_pending": max_ack_pending},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # amount of QoS 1 messages the server can send to
  # a subscription without receiving any PUBACK for those messages
  # The valid range is [0..65535]
  max_ack_pending: {max_ack_pending}
}}
"""
    )


def test_config_with_mqtt_tls(tls_files: TLSCertificates) -> None:
    options = ServerOptions(
        mqtt=MQTT(
            tls=TLS(
                cert_file=tls_files.cert_file,
                key_file=tls_files.key_file,
                ca_file=tls_files.ca_file,
            )
        )
    )
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "mqtt": {
            "tls": {
                "cert_file": tls_files.cert_file,
                "key_file": tls_files.key_file,
                "ca_file": tls_files.ca_file,
            }
        },
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222

# Configure MQTT server
mqtt: {{
  # Configure TLS
  tls: {{
    "ca_file": "{tls_files.ca_file}",
    "cert_file": "{tls_files.cert_file}",
    "key_file": "{tls_files.key_file}"
  }}
}}
"""
    )


def test_config_with_mqtt_and_no_auth_user() -> None:
    account_name = user = password = "test"
    accounts = {account_name: Account(users=[User(user=user, password=password)])}
    options = ServerOptions(accounts=accounts, mqtt=MQTT(no_auth_user=user))
    assert non_null(options) == {
        "host": "0.0.0.0",
        "port": 4222,
        "accounts": non_null(accounts),
        "mqtt": {"no_auth_user": user},
    }
    config = render(options)
    assert config == (
        f"""# Auto-generated
# NATS server listening host
host: 0.0.0.0
# NATS server listening port
port: 4222
# Enable multitenancy using accounts
accounts: {{
  "{account_name}": {{
    "users": [
      {{
        "password": "{password}",
        "user": "{user}"
      }}
    ]
  }}
}}

# Configure MQTT server
mqtt: {{
  # A client connecting without any form of authentication will be associated with this user, its permissions and account
  no_auth_user: "{user}"
}}
"""
    )

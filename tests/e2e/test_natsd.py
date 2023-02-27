from nats_tools.natsd import NATSD
from nats_tools.testing import parametrize_nats_server


def test_natsd_can_be_started_using_context_manager():
    with NATSD(debug=True) as nats:
        assert nats.is_alive()
        assert nats.monitor.healthz() == {"status": "ok"}


def test_natsd_can_be_stopped():
    nats = NATSD(debug=True)
    nats.start(wait=True)
    assert nats.is_alive()
    assert nats.monitor.healthz() == {"status": "ok"}
    nats.stop()
    assert not nats.is_alive()


def test_natsd_can_be_reloaded():
    with NATSD(debug=True, port=4123) as nats:
        assert nats.monitor.healthz() == {"status": "ok"}
        nats.reload_config()
        assert nats.monitor.healthz() == {"status": "ok"}


def test_natsd_fixture_can_be_used_within_tests(natsd: NATSD):
    assert natsd.is_alive()
    assert natsd.monitor.healthz() == {"status": "ok"}


@parametrize_nats_server(port=5000)
def test_parametetrize_nats_server_fixture_can_be_used(natsd: NATSD):
    assert natsd.port == 5000
    assert natsd.is_alive()
    assert natsd.monitor.healthz() == {"status": "ok"}

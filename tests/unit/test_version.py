def test_version() -> None:
    """Test that version string can be imported successfully"""
    from nats_tools import __version__
    from nats_tools.__about__ import __version__ as __about_version__

    assert isinstance(__version__, str)
    assert __version__ == __about_version__

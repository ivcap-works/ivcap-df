from ivcap_df import __version__

def test_version():
    """Test reading version."""
    assert type(__version__) == str

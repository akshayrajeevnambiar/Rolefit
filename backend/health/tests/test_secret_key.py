import pytest
from django.core.exceptions import ImproperlyConfigured

from config.settings import DEV_SECRET_KEY, resolve_secret_key


def test_dev_secret_is_used_only_when_debug_is_on() -> None:
    assert resolve_secret_key(debug=True, configured=None) == DEV_SECRET_KEY
    assert resolve_secret_key(debug=True, configured="") == DEV_SECRET_KEY
    assert resolve_secret_key(debug=True, configured="from-the-env") == "from-the-env"


def test_missing_or_dev_secret_refuses_to_boot_when_debug_is_off() -> None:
    for configured in (None, "", "   ", DEV_SECRET_KEY, f"  {DEV_SECRET_KEY}  "):
        with pytest.raises(ImproperlyConfigured):
            resolve_secret_key(debug=False, configured=configured)


def test_short_secret_refuses_to_boot_when_debug_is_off() -> None:
    """Django's security.W009 asks for 50 characters. Match that floor."""
    short = "k" * 49
    with pytest.raises(ImproperlyConfigured, match="50"):
        resolve_secret_key(debug=False, configured=short)

    long_enough = "k" * 50
    assert resolve_secret_key(debug=False, configured=long_enough) == long_enough
    padded = f"  {long_enough}  "
    assert resolve_secret_key(debug=False, configured=padded) == long_enough

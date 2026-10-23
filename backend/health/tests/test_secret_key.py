import pytest
from django.core.exceptions import ImproperlyConfigured

from config.settings import DEV_SECRET_KEY, resolve_secret_key


def test_dev_secret_is_used_only_when_debug_is_on() -> None:
    assert resolve_secret_key(debug=True, configured=None) == DEV_SECRET_KEY
    assert resolve_secret_key(debug=True, configured="") == DEV_SECRET_KEY
    assert resolve_secret_key(debug=True, configured="from-the-env") == "from-the-env"


def test_missing_or_dev_secret_refuses_to_boot_when_debug_is_off() -> None:
    with pytest.raises(ImproperlyConfigured):
        resolve_secret_key(debug=False, configured=None)
    with pytest.raises(ImproperlyConfigured):
        resolve_secret_key(debug=False, configured="")
    with pytest.raises(ImproperlyConfigured):
        resolve_secret_key(debug=False, configured=DEV_SECRET_KEY)

    assert (
        resolve_secret_key(debug=False, configured="unique-for-this-process")
        == "unique-for-this-process"
    )

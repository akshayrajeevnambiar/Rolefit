"""Settings used by pytest.

The suite uses SQLite in memory so it does not need Postgres. Password
hashing uses MD5 so the auth tests stay fast. The running API does not
import this module.
"""

from config.settings import *  # noqa: F403
from config.settings import REST_FRAMEWORK

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# The real limit is 5/min. Tests sign in more often than that.
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_THROTTLE_RATES": {
        "auth": "1000/min",
    },
}

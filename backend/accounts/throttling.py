"""A small limit on register and login.

Five attempts a minute from one connection. Logout is not limited:
forgetting how to end a session would be worse than ending it twice.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.throttling import SimpleRateThrottle


class AuthRateThrottle(SimpleRateThrottle):
    """Count attempts by the address on the connection.

    DRF's own helper will use X-Forwarded-For when that header is
    present and NUM_PROXIES is unset. A client can invent the header
    and get a fresh limit, so this throttle does not read it.

    The count sits in Django's local memory cache. One dev server
    process means one count. Several processes would each have their own.
    """

    scope = "auth"

    def get_rate(self) -> str:
        rates = settings.REST_FRAMEWORK.get("DEFAULT_THROTTLE_RATES", {})
        try:
            return rates[self.scope]
        except KeyError as exc:
            raise ImproperlyConfigured(
                "DEFAULT_THROTTLE_RATES must include 'auth'."
            ) from exc

    def get_cache_key(self, request, view) -> str:
        address = request.META.get("REMOTE_ADDR") or "unknown"
        return self.cache_format % {"scope": self.scope, "ident": address}

"""Settings for the RoleFit scaffold.

Values come from the environment so secrets stay out of the repo.
See /.env.example for the local placeholders.
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Repo-root .env, if a developer copied .env.example. Existing environment
# variables win, which is what Docker Compose relies on.
load_dotenv(BASE_DIR.parent / ".env")

# Public on purpose. It is in the repo, so it must not sign cookies
# once debug is off.
DEV_SECRET_KEY = "dev-only-not-a-secret"

# Django's security.W009. A shorter key is easier to guess, and this
# process uses the key to sign sessions.
MIN_SECRET_KEY_LENGTH = 50


def resolve_secret_key(*, debug: bool, configured: str | None) -> str:
    """Return the signing key, or refuse to boot.

    The dev placeholder is allowed only while debug is on. Any other
    mode must be given its own key, including when the placeholder is
    still set in the environment. That key must also be at least
    50 characters, which is Django's own floor for SECRET_KEY.
    """
    secret = (configured or "").strip()
    if debug:
        return secret or DEV_SECRET_KEY
    if not secret or secret == DEV_SECRET_KEY:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be a unique value when DJANGO_DEBUG "
            "is not true. The dev placeholder is public."
        )
    if len(secret) < MIN_SECRET_KEY_LENGTH:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must be at least "
            f"{MIN_SECRET_KEY_LENGTH} characters when DJANGO_DEBUG is not true."
        )
    return secret


DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() in {"1", "true", "yes"}
SECRET_KEY = resolve_secret_key(
    debug=DEBUG,
    configured=os.environ.get("DJANGO_SECRET_KEY"),
)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "localhost,127.0.0.1,backend",
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "health",
]

# Email is the sign-in field. Set before the first migration.
AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "rolefit"),
        "USER": os.environ.get("POSTGRES_USER", "rolefit"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "rolefit"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The session cookie is the login. JavaScript cannot read it.
# The CSRF cookie is readable so the browser can copy it into X-CSRFToken.
# SameSite=Lax blocks it on a cross-site POST. Secure stays off because
# this stack speaks plain HTTP on localhost. An HTTPS deploy must turn
# both Secure flags on.
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False

REST_FRAMEWORK = {
    # JSON only. The browsable API stays off.
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    # New routes are private. The health view opts out with AllowAny.
    # Basic auth is omitted: it would repeat the password on every call,
    # and this server speaks plain HTTP.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    # 0: rate limits use the connection address, not X-Forwarded-For.
    # A client can put anything in that header.
    "NUM_PROXIES": 0,
    "DEFAULT_THROTTLE_RATES": {
        "auth": "5/min",
    },
}

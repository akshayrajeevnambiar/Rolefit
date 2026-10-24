from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie

from accounts.views import (
    CsrfCookieView,
    LoginView,
    LogoutView,
    MeView,
    RegisterView,
)

urlpatterns = [
    path("csrf/", ensure_csrf_cookie(CsrfCookieView.as_view()), name="auth-csrf"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
]

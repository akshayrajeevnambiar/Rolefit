"""Register, login, logout, and who is signed in.

The browser keeps a session cookie. DRF only checks the CSRF token
after that cookie is already logged in, so register and login check
it themselves before they set the cookie. Logout is already logged
in, and session authentication checks the token before this view runs.

Django replaces the CSRF cookie on login and logout. The next request
has to send the new value.
"""

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import LoginSerializer, RegisterSerializer
from accounts.throttling import AuthRateThrottle

# The sentence under the sign-in form. The apostrophe is U+2019, as in
# design/system.md, so the screen can show this string unchanged.
MISMATCH = "That email and password don’t match."


def _payload(user: User) -> dict[str, object]:
    return {"id": user.pk, "email": user.email}


class CsrfCookieView(APIView):
    """Set the CSRF cookie. The body is empty.

    No authentication class: a signed-in caller can refresh the cookie
    without already having the token this view is here to issue.
    """

    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, _request: Request) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request: Request) -> Response:
        SessionAuthentication().enforce_csrf(request)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            with transaction.atomic():
                user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            return Response(
                {"email": ["An account with this email already exists."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # login() wants Django's request. The DRF wrapper does not own the session.
        login(request._request, user)
        return Response(_payload(user), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request: Request) -> Response:
        SessionAuthentication().enforce_csrf(request)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The argument is named username. For this user model that value is the email.
        user = authenticate(
            request._request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response({"detail": MISMATCH}, status=status.HTTP_400_BAD_REQUEST)
        login(request._request, user)
        return Response(_payload(user))


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        logout(request._request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """The signed-in account.

    Session authentication checks the CSRF token on this GET too.
    Send the same X-CSRFToken header as on a write.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(_payload(request.user))

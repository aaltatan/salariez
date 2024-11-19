from typing import Any
from pprint import pprint

from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.decorators import user_passes_test
from jwt import ExpiredSignatureError, decode
from ninja.security import SessionAuth



class PermissionAuth(SessionAuth):
    """
    django auth with permissions
    """

    param_name: str = settings.SESSION_COOKIE_NAME

    def __init__(self, csrf: bool = True, perms: list[str] = []) -> None:
        self.perms = perms
        super().__init__(csrf)

    def _get_token(self, request: HttpRequest) -> dict | None:
        authorization: str = request.headers.get("Authorization")
        if authorization:
            _, token_string = authorization.split("Bearer ")

            try:
                return decode(token_string, settings.SECRET_KEY, algorithms=["HS256"])
            except ExpiredSignatureError as e:
                pprint(e)
                return None

    def _get_user(self, request: HttpRequest) -> Any:
        token = self._get_token(request)
        if token:
            user_id = token.get("user_id")
            if user_id:
                User = get_user_model()
                return User.objects.get(pk=user_id)
        else:
            return request.user

    def authenticate(self, request: HttpRequest, key: str | None = None) -> Any:
        user = self._get_user(request)

        if user.is_superuser or user.has_perms(perm_list=self.perms):
            return user

        return None


def superuser_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is a superuser, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

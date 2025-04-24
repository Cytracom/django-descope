import logging

from descope import SESSION_COOKIE_NAME, SESSION_TOKEN_NAME
from descope.exceptions import AuthException
from rest_framework import authentication, exceptions

from django_descope import descope_client, get_descope_user_model
from django_descope.authentication import DescopeAuthentication
from django_descope.conf import settings


logger = logging.getLogger(__name__)


class DescopeTokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, token):
        try:
            validated_session = descope_client.validate_session(token)
        except AuthException as e:
            logger.debug(e)
            raise exceptions.AuthenticationFailed("Invalid token.")

        try:
            username = validated_session[SESSION_TOKEN_NAME][settings.DESCOPE_USERNAME_CLAIM]
        except KeyError:
            logger.error(
                f"Unable to authenticate user- could not find USERNAME_CLAIM="
                f"{settings.DESCOPE_USERNAME_CLAIM} "
                "in Descope JWT"
            )
            if settings.DEBUG:
                raise
            return None

        DescopeUserModel = get_descope_user_model()
        username_field = getattr(DescopeUserModel, "USERNAME_FIELD", "username")

        user, _ = DescopeUserModel.objects.get_or_create(**{username_field: username})
        user.sync(validated_session)
        return user, token


class DescopeSessionAuthentication(authentication.BaseAuthentication):
    _auth = DescopeAuthentication()

    def authenticate(self, request):
        user = self._auth.authenticate(request)
        if user:
            token = request.session.get(SESSION_COOKIE_NAME, "")
            return user, token
        raise exceptions.AuthenticationFailed("Invalid cookie.")

import logging

from django.contrib.auth import login
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from django_descope.authentication import DescopeAuthentication

logger = logging.getLogger(__name__)


class DescopeMiddleware(MiddlewareMixin):
    _auth = DescopeAuthentication()

    def process_request(self, request: HttpRequest):
        user = self._auth.authenticate(request)
        if user:
            login(request, user)

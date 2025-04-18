try:
    import rest_framework
except ImportError:
    raise ModuleNotFoundError(
        "No module named 'django_descope.rest_framework',"
        " make sure to install django_descope with the 'restframework' extra"
    )

from .authentication import DescopeSessionAuthentication, DescopeTokenAuthentication

__all__ = [
    "DescopeSessionAuthentication",
    "DescopeTokenAuthentication",
]
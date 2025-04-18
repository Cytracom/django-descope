from descope import DescopeClient
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from django_descope.conf import settings

descope_client = DescopeClient(
    project_id=settings.DESCOPE_PROJECT_ID,
    management_key=settings.DESCOPE_MANAGEMENT_KEY,
)

def get_descope_user_model():
    """
    Return the DescopeUser model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.DESCOPE_USER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "DESCOPE_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"DESCOPE_USER_MODEL refers to model '{settings.DESCOPE_USER_MODEL}' that has not been installed"
        )

all = [descope_client]

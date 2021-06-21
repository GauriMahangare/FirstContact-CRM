from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="uesfc4g5UBY6y2Sf8gXNQyicYogLm0EKjNEkt4VFenMIoMMMxUUPxdEP35pcGUKA",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "LocalEmails/app-messages"

# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-hosts
# EMAIL_HOST = "localhost"
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-port
# EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405
# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = False
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
    default="amqp://firstcontact_crm:password1@localhost:5672/test_crm",
)
# ------------------------------------------------------------------------------
# Stripe
STRIPE_PUBLIC_KEY = "pk_test_51IHqbQFJjGPNRnAAwoHpztfF08VrSVvJBsLeDSU4We2yX6bBfBxE0YQpMKX2tjmKRwqKjAnOzWfFCKc85EDWJI7l007bxiDRUt"
STRIPE_SECRET_KEY = "sk_test_51IHqbQFJjGPNRnAAqbd6q21BpgKn7QVT74zpI337vBS3tu5W3BkXPR0Ayg7lE8avUK4IbIKlBDITRRusYCD2Q1WX00G8ivzKtG"
STRIPE_WEBHOOK_SECRET = "whsec_wXrSpERbhpdJZpua9URsDYuxZO0m9lnA"

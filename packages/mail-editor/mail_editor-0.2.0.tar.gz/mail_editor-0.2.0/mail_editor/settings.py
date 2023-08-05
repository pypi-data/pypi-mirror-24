import warnings

from django.conf import settings as django_settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured

from .mail_template import Variable


# Available templates and variables for the mail editor.
TEMPLATES = getattr(django_settings, 'MAIL_EDITOR_CONF', {})
if TEMPLATES:
    warnings.warn('Setting MAIL_EDITOR_CONF is deprecated, please use MAIL_EDITOR_TEMPLATES.', DeprecationWarning)
else:
    TEMPLATES = getattr(django_settings, 'MAIL_EDITOR_TEMPLATES', {})


# Location of folder holding "package.json".
PACKAGE_JSON_DIR = getattr(django_settings, 'PACKAGE_JSON_DIR', None)
if PACKAGE_JSON_DIR:
    warnings.warn('Setting PACKAGE_JSON_DIR is deprecated, please use MAIL_EDITOR_PACKAGE_JSON_DIR.', DeprecationWarning)
else:
    PACKAGE_JSON_DIR = getattr(django_settings, 'MAIL_EDITOR_PACKAGE_JSON_DIR', None)


# Location of folder holding "package.json".
ADD_BIN_PATH = getattr(django_settings, 'ADD_BIN_PATH', False)
if ADD_BIN_PATH:
    warnings.warn('Setting ADD_BIN_PATH is deprecated, please use MAIL_EDITOR_ADD_BIN_PATH.', DeprecationWarning)
else:
    ADD_BIN_PATH = getattr(django_settings, 'MAIL_EDITOR_ADD_BIN_PATH', False)


BIN_PATH = getattr(django_settings, 'BIN_PATH', None)
if BIN_PATH:
    warnings.warn('Setting BIN_PATH is deprecated, please use MAIL_EDITOR_BIN_PATH.', DeprecationWarning)
else:
    BIN_PATH = getattr(django_settings, 'MAIL_EDITOR_BIN_PATH', False)


# The base URL when relative links are found.
BASE_URL = getattr(django_settings, 'MAIL_EDITOR_BASE_URL', None)
if not BASE_URL:
    raise ImproperlyConfigured('The setting MAIL_EDITOR_BASE_URL must be configured.')


def get_choices():
    choices = []
    for key, values in TEMPLATES.items():
        choices += [(key, values.get('name'))]
    return choices


def get_config():
    config = {}
    for key, values in TEMPLATES.items():
        subject_variables = []
        for var in values.get('subject', []):
            subject_variables.append(Variable(**var))

        body_variables = []
        for var in values.get('body', []):
            body_variables.append(Variable(**var))

        config[key] = {
            'subject': subject_variables,
            'body': body_variables
        }
    return config

import sys
try:
    from .secrets import *
except ImportError:
    sys.exit('secrets.py settings file not found. Please run `prepare.sh` to create one.')

from .base import *

INSTALLED_APPS += (
    'test_utils',
#    'devserver'
    )

# Support legacy passwords

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COWRY_LIVE_PAYMENTS = False

SELENIUM_TESTS = False
# SELENIUM_WEBDRIVER = 'phantomjs'

COWRY_RETURN_URL_BASE = 'http://localhost:8000'

CRAWLABLE_PHANTOMJS_DEDICATED_MODE = False


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    }

from django.conf import settings
from django.utils.unittest.case import skipUnless, skip
from onepercentclub.tests.utils import OnePercentSeleniumTestCase


@skipUnless(getattr(settings, 'SELENIUM_TESTS', False),
        'Selenium tests disabled. Set SELENIUM_TESTS = True in your settings.py to enable.')
class MemberSettingsTests(OnePercentSeleniumTestCase):

    """ Confirm login failure works """
    def test_failed_login(self):
        self.assertFalse(self.login('fake@example.com', 'fake', wait_time=10))

        # Should see an error message
        self.assertTrue(self.browser.is_text_present('Unable to login', wait_time=30))

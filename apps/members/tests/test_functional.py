from django.conf import settings
from django.utils.unittest.case import skipUnless, skip
from onepercentclub.tests.utils import OnePercentSeleniumTestCase


@skipUnless(getattr(settings, 'SELENIUM_TESTS', False),
        'Selenium tests disabled. Set SELENIUM_TESTS = True in your settings.py to enable.')
class MemberSettingsTests(OnePercentSeleniumTestCase):

    """ Confirm login failure works """
    @skip('Skip failed login on wrong credentials for now.')
    def test_failed_login(self):
        self.login('fake@example.com', 'fake', wait_time=30)

        # Should see an error message
        self.assert_css('.modal-flash-message', wait_time=2)

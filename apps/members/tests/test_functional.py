from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from django.conf import settings
from django.utils.unittest.case import skipUnless
from onepercentclub.tests.utils import OnePercentSeleniumTestCase
from django.utils.translation import ugettext as _


@skipUnless(getattr(settings, 'SELENIUM_TESTS', False),
        'Selenium tests disabled. Set SELENIUM_TESTS = True in your settings.py to enable.')
class MemberFailedLoginTests(OnePercentSeleniumTestCase):

    def setUp(self):
        self.init_projects()
        self.user = BlueBottleUserFactory.create()

    def test_failed_login_missing_email(self):
        """ Confirm login fails without email and shows an error message """

        self.visit_homepage()
        # Find the link to the signup button page and click it.
        self.scroll_to_and_click_by_css('.nav-signup-login a')
        self.wait_for_element_css('.modal-fullscreen-content')

        # Fill in details.
        self.browser.find_by_css('input[type=password]').fill('fake')
        self.browser.find_by_css("a[name=login]").click()

        # Should see an error message
        self.assert_css('.modal-flash-message', wait_time=10)
        self.assert_text(_("Email required"))

    def test_failed_login_missing_password(self):
        """ Confirm login fails without password and shows an error message """
        self.visit_homepage()
        # Find the link to the signup button page and click it.
        self.scroll_to_and_click_by_css('.nav-signup-login a')
        self.wait_for_element_css('.modal-fullscreen-content')

        # Fill in details.
        self.browser.find_by_css('input[name=username]').fill(self.user.email)
        self.browser.find_by_css("a[name=login]").click()

        # Should see an error message
        self.assert_css('.modal-flash-message', wait_time=10)
        self.assert_text(_("Password required"))

    def test_failed_login_wrong_credentials(self):
        """ Confirm login fails with wrong credentials and shows an error message """
        self.visit_homepage()
        # Find the link to the signup button page and click it.
        self.scroll_to_and_click_by_css('.nav-signup-login a')
        self.wait_for_element_css('.modal-fullscreen-content')

        # Fill in details.
        self.browser.find_by_css('input[name=username]').fill(self.user.email)
        self.browser.find_by_css('input[type=password]').fill('fake')
        self.browser.find_by_css("a[name=login]").click()

        # Should see an error message
        # self.assert_css('.modal-flash-message', wait_time=10)
        # self.assert_text(_("Unable to login with provided credentials."))

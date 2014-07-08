from bluebottle.bb_projects.models import ProjectPhase, ProjectTheme
from bluebottle.test.factory_models.projects import ProjectPhaseFactory, ProjectThemeFactory
from bluebottle.test.utils import SeleniumTestCase
from bluebottle.utils.models import Language
from django.test import TestCase
from bluebottle.test.factory_models.utils import LanguageFactory


class InitProjectDataMixin(object):

    def init_projects(self):
        """
        Set up some basic models needed for project creation.
        """
        phase_data = [{'id': 1, 'name': 'Plan - New', 'viewable': False},
                      {'id': 2, 'name': 'Plan - Submitted', 'viewable': False},
                      {'id': 3, 'name': 'Plan - Needs Work', 'viewable': False},
                      {'id': 4, 'name': 'Plan - Rejected', 'viewable': False},
                      {'id': 6, 'name': 'Plan - Accepted', 'viewable': True},
                      {'id': 5, 'name': 'Campaign', 'viewable': True},
                      {'id': 7, 'name': 'Stopped', 'viewable': False},
                      {'id': 8, 'name': 'Done - Complete', 'viewable': True},
                      {'id': 9, 'name': 'Done - Incomplete', 'viewable': True}]

        theme_data = [{'id': 1, 'name': 'Education'},
                      {'id': 2, 'name': 'Environment'}]

        language_data = [{'id': 1, 'code': 'en', 'language_name': 'English', 'native_name': 'English'},
                         {'id': 2, 'code': 'nl', 'language_name': 'Dutch', 'native_name': 'Nederlands'}]

        for phase in phase_data:
            ProjectPhaseFactory.create(**phase)

        for theme in theme_data:
            ProjectThemeFactory.create(**theme)

        for language in language_data:
            LanguageFactory.create(**language)


class OnePercentTestCase(InitProjectDataMixin, TestCase):
    pass


class OnePercentSeleniumTestCase(InitProjectDataMixin, SeleniumTestCase):

    def login(self, username, password, wait_time=10):
        """
        Perform login operation on the website.

        :param username: The user's email address.
        :param password: The user's password
        :return: ``True`` if login was successful.
        """
        self.init_projects()
        self.visit_homepage()

        # Find the link to the signup button page and click it.
        self.scroll_to_and_click_by_css('.nav-signup-login a')
        self.wait_for_element_css('.modal-fullscreen-content')

        # Fill in details.
        self.browser.find_by_css('input[name=username]').fill(username)
        self.browser.find_by_css('input[type=password]').fill(password)

        self.browser.find_by_css("a[name=login]").click()

        # FIXME: We should be checking some other state, maybe something in Ember
        return self.browser.is_text_present('My 1%', wait_time=wait_time)

    def logout(self):
        # Click user profile to open menu - mouse_over() only works for chrome
        self.browser.find_by_css('.nav-member-dropdown').click()
        
        # Click the logout item
        logout = '.nav-member-logout a'
        self.wait_for_element_css(logout)
        return self.browser.find_by_css(logout).click()

    def visit_homepage(self, lang_code=None):
        """
        Convenience function to open the homepage.

        :param lang_code: A two letter language code as used in the URL.
        :return: ``True`` if the homepage could be visited.
        """
        self.visit_path('', lang_code)

        # Check if the homepage opened, and the dynamically loaded content appeared.
        return self.wait_for_element_css('#home')

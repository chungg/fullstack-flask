import os
import re

from playwright.sync_api import expect, Page

from tests.system.pages.login import LoginPage


def test_valid_login(page: Page) -> None:
    login_page = LoginPage(page)

    # navigate to login page
    login_page.load()

    # login
    login_page.login(os.environ['TEST_USER'], os.environ['TEST_PW'])

    # validate redirected to root
    expect(page).to_have_url('http://127.0.0.1:5000/')


def test_invalid_login(page: Page) -> None:
    login_page = LoginPage(page)

    # navigate to login page
    login_page.load()

    # login
    login_page.login(os.environ['TEST_USER'], 'not_right_password')

    # check still on login page and warnings displayed
    expect(page).to_have_url(login_page.URL)
    expect(page.locator('//button[normalize-space()="Login"]')).to_have_class(
        re.compile(r'is-danger'))
    expect(page.get_by_placeholder('Email')).to_have_value(os.environ['TEST_USER'])

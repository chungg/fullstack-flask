from playwright.sync_api import Page


class LoginPage:

    URL = 'http://127.0.0.1:5000/api/login'

    def __init__(self, page: Page) -> None:
        self.page = page

    def load(self) -> None:
        self.page.goto(self.URL)

    def login(self, email, pw) -> None:
        self.page.get_by_placeholder('Email').fill(email)
        self.page.locator('//input[@name="password"]').fill(pw)
        self.page.locator('//p/button[normalize-space()="Login"]').click()

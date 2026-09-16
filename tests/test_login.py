from playwright.sync_api import sync_playwright, Page, expect
from pages.loginPage import LoginPage
from pages.homePage import homePage
import pytest

@pytest.mark.real_login
def test_positive_login(page:Page, navigateToAmazon, credentials):
  loginPageObj = LoginPage(page)
  homePageObj = homePage(page)
  homePageObj.navigate_to_login()
  loginPageObj.enter_email(credentials["email"])
  loginPageObj.enter_password(credentials["password"])
  expect(page).to_have_title("Online Shopping site in India: Shop Online for Mobiles, Books, Watches, Shoes and More - Amazon.in")

def test_negative_login(page:Page, navigateToAmazon):
  loginPageObj = LoginPage(page)
  homePageObj = homePage(page)
  homePageObj.navigate_to_login()
  loginPageObj.enter_email("invalid_email_test_12345domain.com")
  expect(loginPageObj.invalid_email_error_msg).to_be_visible()
  loginPageObj.enter_email("invalid_email_test_12345@domain.com")
  expect(loginPageObj.newAccountMsg).to_be_visible()


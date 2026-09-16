from playwright.sync_api import Page, sync_playwright, expect
from pages.homePage import homePage

def test_validatePageComponents(page:Page, navigateToAmazon):
  expect(page).to_have_title("Online Shopping site in India: Shop Online for Mobiles, Books, Watches, Shoes and More - Amazon.in")
  expect(page).to_have_url("https://www.amazon.in/")

def test_validateTheVisibilityofPageComponents(page:Page, navigateToAmazon):
  homePageObj = homePage(page)
  homePageObj.validateTheVisibilityOfSearchBar()
  homePageObj.validateTheVisibilityOfCartIcon()
  homePageObj.validateTheVisibilityOfAmazonLogo()

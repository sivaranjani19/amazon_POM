import pytest
from playwright.sync_api import sync_playwright, Page, expect
from pages.homePage import homePage
from pages.productPage import productPage
from pages.resultsPage import resultsPage

# depends on which product the live search returns; some require a variant selection that this test doesn't handle.
@pytest.mark.flaky_live_site
def test_add_to_cart(page: Page, navigateToAmazon):
  homePageObj = homePage(page)
  before_count = 0
  resultsPageObj = resultsPage(page)
  homePageObj.fillSearchBox()
  homePageObj.clickOnSearchBtn()
  resultsPageObj.validateTheVisibilityOfResultsText()
  new_page = resultsPageObj.clickFirstResult(page)
  productsPageObj = productPage(new_page)
  productsPageObj.addToShoppingCart()
  expect(productsPageObj.cart_count).to_have_text(str(before_count + 1))
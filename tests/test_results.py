from playwright.sync_api import sync_playwright, Page, expect
from pages.homePage import homePage
from pages.resultsPage import resultsPage
def test_validateTheresultsUI(page: Page, navigateToAmazon):
  homePageObj = homePage(page)
  homePageObj.fillSearchBox()
  homePageObj.clickOnSearchBtn()
  resultsPageObj = resultsPage(page)
  resultsPageObj.validateTheVisibilityOfResultsText()

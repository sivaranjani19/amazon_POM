from playwright.sync_api import sync_playwright, Page, expect
from pages.homePage import homePage
from pages.resultsPage import resultsPage

def test_search_shows_results_for_query(page: Page, navigateToAmazon):
  homePageObj = homePage(page)
  homePageObj.fillSearchBox()
  homePageObj.clickOnSearchBtn()
  resultsPageObj = resultsPage(page)
  resultsPageObj.validateTheVisibilityOfResultsText()

def test_empty_search_stays_on_home(page: Page, navigateToAmazon):
  homePageObj = homePage(page)
  resultsPageObj = resultsPage(page)
  homePageObj.clickOnSearchBtn()
  resultsPageObj.validateNoResultsPageShown()
  resultsPageObj.validateStillOnHomePage(page)


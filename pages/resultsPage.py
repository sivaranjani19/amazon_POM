from playwright.sync_api import sync_playwright, Page, expect

class resultsPage():
  def __init__(self, page):
    self.resultsText = page.get_by_role("heading", name="results for", level=2)
    self.first_product_link = (
            page.locator("div[data-component-type='s-search-result']")
            .first
            .get_by_role("link")
            .filter(has=page.get_by_role("heading"))
    )

  def validateTheVisibilityOfResultsText(self):
    expect(self.resultsText).to_be_visible()

  def validateNoResultsPageShown(self):
    expect(self.resultsText).not_to_be_visible()

  def validateStillOnHomePage(self, page):
    expect(page).to_have_url("https://www.amazon.in/")

  def clickFirstResult(self, page):
    with page.expect_popup() as popup_info:
      self.first_product_link.click()
    new_page = popup_info.value
    return new_page

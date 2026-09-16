from playwright.sync_api import sync_playwright, Page, expect

class resultsPage():
  def __init__(self, page):
    self.resultsText = page.get_by_role("heading", name="Results", exact=True)

  def validateTheVisibilityOfResultsText(self):
    expect(self.resultsText).to_be_visible()
from playwright.sync_api import expect, sync_playwright, Page

class homePage:
  def __init__(self, page):
    self.searchBarTxtBox = page.locator("#twotabsearchtextbox")
    self.cartIcon = page.locator("#nav-cart-count-container")
    self.logo = page.locator("#nav-logo-sprites")
    self.searchBtn =  page.get_by_role("button", name="Go", exact=True)
    self.sign_in_link = page.get_by_role("link",name="Account & Lists")

  def navigate_to_login(self):
    self.sign_in_link.click()

  def validateTheVisibilityOfSearchBar(self):
    expect(self.searchBarTxtBox).to_be_visible()

  def validateTheVisibilityOfCartIcon(self):
    expect(self.cartIcon).to_be_visible()

  def validateTheVisibilityOfAmazonLogo(self):
    expect(self.logo).to_be_visible()

  def fillSearchBox(self):
    self.searchBarTxtBox.fill("iphone")

  def clearSearchBox(self):
    self.searchBarTxtBox.clear()

  def clickOnSearchBtn(self):
     self.searchBtn.click()


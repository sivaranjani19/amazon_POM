from playwright.sync_api import sync_playwright, Page, expect

class productPage():
  def __init__(self, page):
    self.add_to_cart_btn = page.get_by_role("button", name="Add to cart")
    self.cart_count = page.locator("#nav-cart-count-container")

  def addToShoppingCart(self):
    self.add_to_cart_btn.click()




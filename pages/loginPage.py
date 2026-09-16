from playwright.sync_api import sync_playwright, Page, expect

class LoginPage():
  def __init__(self, page):

    self.email_input = page.get_by_role("textbox", name="email")
    self.password_input = page.get_by_role("textbox", name="password")
    self.continue_btn = page.get_by_role("button", name="Continue")
    self.submit_btn = page.locator("#signInSubmit")
    self.invalid_email_error_msg = page.get_by_text("Invalid email address")
    self.newAccountMsg = page.get_by_text("It looks like you are new to Amazon")



  def enter_email(self, email: str):
    self.email_input.fill(email)
    self.continue_btn.click()

  def enter_password(self, password: str):
      self.password_input.fill(password)
      self.submit_btn.click()


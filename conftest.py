from playwright.sync_api import Page, expect, sync_playwright
from dotenv import load_dotenv
import pytest
import os

load_dotenv()

@pytest.fixture
def navigateToAmazon(page: Page):
  page.goto("https://www.amazon.in/")
  #page.locator("#twotabsearchtextbox")

@pytest.fixture
def credentials():
  return {
    "email": os.getenv("AMAZON_EMAIL"),
    "password": os.getenv("AMAZON_PASSWORD"),
  }
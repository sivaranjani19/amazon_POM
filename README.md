# Amazon UI Automation (Page Object Model)

A UI test automation suite against [amazon.in](https://www.amazon.in/), built with Python, pytest, and Playwright's browser automation client (via the `pytest-playwright` plugin). This project was built to demonstrate front-end test automation and the Page Object Model (POM) pattern: encapsulated page classes, accessibility-first locators, positive/negative UI test design, and a CI pipeline with a published test report.

**Live test report:** https://sivaranjani19.github.io/amazon_POM/
(auto-published on every push to `main` and every nightly run)

## Tech Stack

- **Python** + **pytest** — test runner and assertions
- **Playwright** (via **pytest-playwright**) — browser automation; used here specifically because this project drives a real browser UI, unlike the [api-testing-playwright](https://github.com/sivaranjani19/api-testing-playwright) project, which deliberately avoids this plugin since it only makes HTTP requests
- **python-dotenv** — loads real account credentials from a local `.env` file, never hardcoded in test code
- **pytest-html** — generates the HTML test report
- **GitHub Actions** — CI, running on push and a nightly schedule

## Architecture

### Page Object Model (`pages/`)

Each page of the site under test has its own class encapsulating its locators and the actions available on it:

- **`LoginPage`** — email/password inputs, continue/submit buttons, and the error/new-account messages Amazon shows depending on what you enter. `enter_email()` and `enter_password()` take the value as a parameter, so the page object has no knowledge of *whose* credentials it's entering — that decision belongs to the test.
- **`homePage`** — search bar, cart icon, logo, sign-in link, plus visibility assertions for each.
- **`resultsPage`** — the search results list, including a locator for the first organic (non-sponsored) product link, built structurally (`div[data-component-type='s-search-result']`, filtered to the link containing a heading) rather than matched on product text, since the actual products returned change per search and over time.
- **`productPage`** — a product's own detail page: the "Add to Shopping Cart" button and the header's live cart-count badge.

Locators are built with Playwright's accessibility-first selectors (`get_by_role`, `get_by_text`) rather than brittle CSS selectors, matching current Playwright best practice — with targeted exceptions where Amazon's markup makes that impractical (see Known Limitations).

### Fixtures (`conftest.py`)

- **`navigateToAmazon`** — navigates to `amazon.in` at the start of a test, so every test starts from the same known page.
- **`credentials`** — loads `AMAZON_EMAIL`/`AMAZON_PASSWORD` from environment variables (via `python-dotenv` locally) and returns them as a dict, so no test file ever contains a real password.

### Secrets

Real account credentials are never hardcoded. `AMAZON_EMAIL` and `AMAZON_PASSWORD` are read via `os.getenv()`, sourced from a local `.env` file (gitignored, never committed).

### Skipping unreliable-in-CI tests

Two tests are excluded from CI via custom pytest markers (registered in `pytest.ini`), each for a different reason — both still run locally:

- **`real_login`** (`test_positive_login`) — performs an actual login against production amazon.in. Running that from CI runners would hit Amazon's bot detection (shared/rotating IPs are exactly what that looks for) and risks flagging or locking the real account behind it.
- **`flaky_live_site`** (`test_add_to_cart`) — see Known Limitations below.

CI runs `pytest -m "not real_login and not flaky_live_site"`.

## Test Coverage

### Login (`tests/test_login.py`)
- **Positive login** (`test_positive_login`, local-only — see above) — logs in with real credentials from the `credentials` fixture, verifies the post-login page title.
- **Negative login** (`test_negative_login`) — invalid email format triggers Amazon's inline validation error; a syntactically valid but unregistered email triggers Amazon's "new to Amazon" messaging. No real credentials involved.

### Home page (`tests/test_home.py`)
- Page title/URL assertions on load.
- Visibility checks for the search bar, cart icon, and Amazon logo via `homePage`'s dedicated assertion methods.

### Search results (`tests/test_results.py`)
- **`test_search_shows_results_for_query`** — searches, then asserts the results-count heading is showing (via a locator scoped to the correct heading level, to avoid matching Amazon's duplicate nav-ribbon text with the same words).
- **`test_empty_search_stays_on_home`** — clicking search with nothing typed should never produce a results page; asserts both that the results heading never appears and that the URL stays on the home page.

### Add to cart (`tests/test_products.py`)
- **`test_add_to_cart`** (local-only — see Known Limitations) — searches, opens the first organic result (handling the new-tab popup every product link opens into), adds it to cart, and asserts the header's cart-count badge goes from `0` to `1` using an auto-retrying `expect(...).to_have_text(...)` assertion, since the badge updates asynchronously after the click.

## Running Locally

```bash
git clone https://github.com/sivaranjani19/amazon_POM.git
cd amazon_POM
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create a `.env` file in the project root with your own Amazon credentials:
```
AMAZON_EMAIL=your_email_here
AMAZON_PASSWORD=your_password_here
```

Run the tests:
```bash
pytest -v
```

Run only what's safe for CI:
```bash
pytest -m "not real_login and not flaky_live_site" -v
```

Generate an HTML report:
```bash
pytest --html=report.html --self-contained-html
```

## Known Limitations

### `test_add_to_cart` depends on uncontrollable live product data

Every product link on Amazon's results page opens in a new tab (`page.expect_popup()`), discovered by recording the real flow with Playwright's `codegen` tool rather than guessing at it. Beyond that, this test's reliability depends on *which specific product* the live "iphone" search happens to return as the first organic result: some products allow "Add to Shopping Cart" immediately, while others require selecting a variant (storage, color) first, which silently no-ops the click instead of adding the item. Since search results rotate and aren't something a test can control, this test sometimes fails for reasons unrelated to the code under test.

Rather than building a generic handler for Amazon's many different variant-selection UIs — disproportionate effort for one portfolio test — this is marked `flaky_live_site` and excluded from CI, with the reason documented here and in the test file itself. It's left runnable locally as a demonstration of the full add-to-cart flow, including handling the new-tab navigation and the async cart-badge update (`expect(...).to_have_text(...)`, not a plain read-and-compare, since the badge updates after a delay following the click).

## CI/CD

`.github/workflows/tests.yml` runs the suite (excluding `real_login`- and `flaky_live_site`-marked tests):
- On every push to `main`
- On a nightly schedule (3 AM UTC)

Each run installs dependencies, installs the Chromium browser, runs the tests headlessly against the live site, and publishes the resulting HTML report to GitHub Pages — so the latest results are always viewable at the link above, pass or fail.

## Possible Next Steps

- Detect when a product page requires a variant selection and handle it, to make `test_add_to_cart` reliable enough for CI
- Add cross-browser runs (Firefox, WebKit) alongside the current Chromium-only CI run

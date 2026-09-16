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
- **`resultsPage`** — assertions on the search results page after a search is performed.

Locators are built with Playwright's accessibility-first selectors (`get_by_role`, `get_by_text`) rather than brittle CSS selectors, matching current Playwright best practice.

### Fixtures (`conftest.py`)

- **`navigateToAmazon`** — navigates to `amazon.in` at the start of a test, so every test starts from the same known page.
- **`credentials`** — loads `AMAZON_EMAIL`/`AMAZON_PASSWORD` from environment variables (via `python-dotenv` locally) and returns them as a dict, so no test file ever contains a real password.

### Secrets

Real account credentials are never hardcoded. `AMAZON_EMAIL` and `AMAZON_PASSWORD` are read via `os.getenv()`, sourced from a local `.env` file (gitignored, never committed).

### Skipping the live-login test in CI

`test_positive_login` performs an actual login against production amazon.in. Running that automatically from CI runners would hit Amazon's bot detection (shared/rotating IPs are exactly what that looks for) and risks flagging or locking the real account behind it. It's marked with a custom `real_login` pytest marker (registered in `pytest.ini`) and excluded from CI runs via `pytest -m "not real_login"`. It still runs locally to demonstrate the full login flow.

## Test Coverage

### Login (`tests/test_login.py`)
- **Positive login** (`test_positive_login`, local-only — see above) — logs in with real credentials from the `credentials` fixture, verifies the post-login page title.
- **Negative login** (`test_negative_login`) — invalid email format triggers Amazon's inline validation error; a syntactically valid but unregistered email triggers Amazon's "new to Amazon" messaging. No real credentials involved.

### Home page (`tests/test_home.py`)
- Page title/URL assertions on load.
- Visibility checks for the search bar, cart icon, and Amazon logo via `homePage`'s dedicated assertion methods.

### Search results (`tests/test_results.py`)
- Full search flow — fill the search box, click search, assert the results page renders the expected content.

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

Run only what's safe for CI (skips the live-login test):
```bash
pytest -m "not real_login" -v
```

Generate an HTML report:
```bash
pytest --html=report.html --self-contained-html
```

## CI/CD

`.github/workflows/tests.yml` runs the suite (excluding `real_login`-marked tests):
- On every push to `main`
- On a nightly schedule (3 AM UTC)

Each run installs dependencies, installs the Chromium browser, runs the tests headlessly against the live site, and publishes the resulting HTML report to GitHub Pages — so the latest results are always viewable at the link above, pass or fail.

## Possible Next Steps

- Extend POM coverage to the cart and checkout flow
- Add cross-browser runs (Firefox, WebKit) alongside the current Chromium-only CI run

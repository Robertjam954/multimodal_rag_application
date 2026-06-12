"""End-to-end Playwright tests against a running backend + built frontend."""
import os

import pytest

pytestmark = pytest.mark.e2e


@pytest.mark.skip(reason="Run after `npm run build && quart run`")
def test_chat_flow_renders_answer():
    from playwright.sync_api import sync_playwright

    base = os.getenv("APP_URL", "http://localhost:50505")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(base)
        page.fill('textarea[placeholder*="Ask"]', "what is chunking?")
        page.click('button:has-text("Send")')
        page.wait_for_selector("text=Verifier", timeout=15000)
        browser.close()

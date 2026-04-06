from typing import Generator

import pytest
from patchright.sync_api import Browser, sync_playwright

from sunarp_service import SunarpNotario
from tests import cp


@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    """Fixture to create a browser instance."""

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, channel="msedge")
        yield browser
        browser.close()


@pytest.fixture
def sunarp_service(browser_instance) -> Generator[SunarpNotario, None, None]:
    """Fixture to create a SunarpNotario service instance."""
    browser_ctx = browser_instance.new_context()
    yield SunarpNotario(browser_ctx)
    browser_ctx.close()


@pytest.fixture
def sunarp_service_logged(sunarp_service) -> Generator[SunarpNotario, None, None]:
    sunarp_service.login(
        cp.get("CREDENTIALS", "SUNARP_USERNAME"),
        cp.get("CREDENTIALS", "SUNARP_PASSWORD"),
    )
    assert "https://sid.sunarp.gob.pe/sid/login.htm" in sunarp_service.page.url

    yield sunarp_service

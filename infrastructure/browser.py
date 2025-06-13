from dataclasses import dataclass, field
from logging import Logger
import random
from typing import Any, Optional
from playwright.async_api import async_playwright, Playwright, Page, BrowserContext

from infrastructure.base_browser import BrowserClient, BrowserLauncher
from infrastructure.config_browser import BrowserConfig


@dataclass
class BrowserManager(BrowserLauncher):
    """
    A concrete implementation of BrowserLauncher that manages browser instances.
    """
    config: BrowserConfig
    logger: Logger
    _playwright: Optional[Any] = field(default=None, init=False)
    _browser: Optional[Any] = field(default=None, init=False)

    async def launch(self) -> tuple[BrowserContext, BrowserClient]:
        playwright = await async_playwright().start()
        browser = await self._launch_browser(playwright)
        context = await browser.new_context(
            user_agent=self.config.user_agent,
            extra_http_headers=self.config.custom_headers,
        )
        page = await context.new_page()
        if self.config.stealth_mode:
            await self._apply_stealth_mode(page)
        return context, page

    async def _launch_browser(self, playwright: Playwright) -> BrowserClient:
        launch_options = {
            # 'args': ['--disable-http2'],
            'headless': self.config.headless,
            'proxy': {'server': self.config.proxy} if self.config.proxy else None,
            'timeout': self.config.timeout
        }
        if self.config.browser_type == "firefox" and self.config.stealth_mode:
            launch_options["firefox_user_prefs"] = {
                "privacy.resistFingerprinting": True,
                "privacy.trackingprotection.enabled": True
            }
        return await getattr(playwright, self.config.browser_type).launch(**launch_options)

    async def _apply_stealth_mode(self, page: Page) -> None:
        await page.add_init_script(self.config.stealth_script)

    async def close(self) -> None:
        try:
            if self._browser:
                await self._browser.close()
            if self._playwright:
                await self._playwright.stop()
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {str(e)}")


@dataclass
class PageInteractor:
    """
    A class to interact with the browser page.
    """
    client: BrowserClient
    logger: Logger

    async def navigate(self, url: str) -> None:
        self.logger.info(f"Navigating to {url}")
        await self.client.goto(url)

    async def fill_input(self, selector: str, value: str) -> None:
        self.logger.info(f"Filling input {selector} with value {value}")
        await self.client.fill(selector, value)
        await self.random_delay(300, 900)

    async def click_element(self, selector: str) -> None:
        self.logger.info(f"Clicking element {selector}")
        await self.client.click(selector)
        await self.random_delay(300, 800)

    async def wait_for_element(self, selector: str) -> None:
        self.logger.info(f"Waiting for element {selector}")
        await self.client.wait_for_selector(selector)
        await self.random_delay(100, 500)

    async def inner_text(self, selector: str) -> str:
        self.logger.info(f"Getting inner text of {selector}")
        text = await self.client.inner_text(selector)
        await self.random_delay(100, 200)
        return text

    async def handle_popup(self, popup_selector: str, action: str = "accept") -> None:
        if await self.client.query_selector(popup_selector):
            if action == "accept":
                await self.click_element(f"{popup_selector} .accept-btn")
            elif action == "dismiss":
                await self.click_element(f"{popup_selector} .dismiss-btn")
            await self.random_delay(1000, 2000)

    async def random_delay(self, min_ms: int, max_ms: int) -> None:
        await self.client.wait_for_timeout(random.randint(min_ms, max_ms))


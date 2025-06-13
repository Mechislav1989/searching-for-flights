from dataclasses import dataclass, field
from logging import Logger
from typing import Optional

from infrastructure.base_browser import BrowserClient, BrowserLauncher
from infrastructure.browser import PageInteractor
from infrastructure.config_browser import SelectorConfig
from infrastructure.data_parser import DataParser
from infrastructure.error_handler import ErrorHandler


@dataclass
class BrowserService:
    launcher: BrowserLauncher
    logger: Logger
    selector_config: SelectorConfig
    _client: Optional[BrowserClient] = field(default=None, init=False)
    _interactor: Optional[PageInteractor] = field(default=None, init=False)
    _parser: Optional[DataParser] = field(default=None, init=False)

    async def __aenter__(self):
        self._client = await self.launcher.launch()
        self._interactor = PageInteractor(self._client, self.logger)
        self._parser = DataParser(self._client, self.selector_config, self.logger)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                error_handler = ErrorHandler(self.logger)
                await error_handler.handle_error(self._client, exc_val)
        finally:
            if self._client:
                await self.launcher.close(self._client)
            self._client = None
            self._interactor = None
            self._parser = None

    @property
    def selectors(self) -> SelectorConfig:
        return self.selector_config

    @property
    def client(self) -> BrowserClient:
        if self._client is None:
            raise RuntimeError("Browser client not initialized")
        return self._client

    @property
    def interactor(self) -> PageInteractor:
        if self._interactor is None:
            raise RuntimeError("PageInteractor not initialized")
        return self._interactor

    @property
    def parser(self) -> DataParser:
        if self._parser is None:
            raise RuntimeError("DataParser not initialized")
        return self._parser
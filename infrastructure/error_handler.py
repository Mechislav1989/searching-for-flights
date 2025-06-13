from dataclasses import dataclass
from logging import Logger

from infrastructure.base_browser import BrowserClient


@dataclass
class ErrorHandler:
    logger: Logger
    error_count: int = 0

    async def handle_error(self, client: BrowserClient, error: Exception):
        self.error_count += 1
        self.logger.error(f"Error occurred: {str(error)}")
        await self._capture_evidence(client)


@dataclass
class ConsoleLogger(Logger):
    name: str = "BrowserService"
    
    def info(self, message: str) -> None:
        print(f"[INFO][{self.name}] {message}")
    
    def error(self, message: str) -> None:
        print(f"[ERROR][{self.name}] {message}")
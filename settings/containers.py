from functools import lru_cache
from logging import Logger

import punq

from application.usecases.searches_for_flights import FlightSearchUseCase
from infrastructure.base_browser import BrowserLauncher
from infrastructure.browser import BrowserManager
from infrastructure.browser_service import BrowserService
from infrastructure.config_browser import BrowserConfig, SelectorConfig
from infrastructure.error_handler import ConsoleLogger


@lru_cache(1)
def get_container() -> punq.Container:
    """
    Returns a singleton instance of the punq container.
    """
    return _init_container()


def _init_container() -> punq.Container:
    """
    Initializes the punq container with the necessary bindings.
    """
    container = punq.Container()

    # Configurations (singleton)
    container.register(BrowserConfig, instance=BrowserConfig(), scope=punq.Scope.singleton)
    
    container.register(SelectorConfig, instance=SelectorConfig(), scope=punq.Scope.singleton)
    
    # Registration of abstractions with implementations
    container.register(Logger, factory=ConsoleLogger)
    container.register(BrowserLauncher, factory=BrowserManager)
    
    container.register(BrowserService, factory=lambda: BrowserService(
        launcher=container.resolve(BrowserLauncher),
        logger=container.resolve(Logger),
        selector_config=container.resolve(SelectorConfig)
    ))
    
    container.register(FlightSearchUseCase, factory=lambda: FlightSearchUseCase(
        browser_service=container.resolve(BrowserService),
        logger=container.resolve(Logger)
    ))
    
    return container

from dataclasses import dataclass
from logging import Logger

from domain.entities.flight import Flight

from infrastructure.base_browser import BrowserClient
from infrastructure.config_browser import SelectorConfig


@dataclass
class DataParser:
    client: BrowserClient
    selectors: SelectorConfig
    logger: Logger

    async def parse_flight_data(self) -> list[Flight]:
        self.logger.info("Parsing flight data")
        try:
            await self.client.wait_for_selector(self.selectors.result_items)
        except Exception as e:
            self.logger.error(f"Error waiting for flight results: {e}")
            return []    
        flight_elements = await self.client.query_selector_all(self.selectors.result_items)
        
        flights = [
            Flight(
                airline=await flight.inner_text(self.selectors.airline),
                departure=await flight.inner_text(self.selectors.departure),
                arrival=await flight.inner_text(self.selectors.arrival),
                duration=await flight.inner_text(self.selectors.duration),
                price=await flight.inner_text(self.selectors.flight_cost),
                stop=await flight.inner_text(self.selectors.stop),
            )
            for flight in flight_elements
        ]
        
        self.logger.info(f"Found {len(flights)} flights")
        return flights
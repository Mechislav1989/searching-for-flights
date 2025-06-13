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
        self.logger.info(f"Found {len(flight_elements)} flight elements")
        flights = []
        for el in flight_elements:
            airline_el = await el.query_selector(self.selectors.airline)
            departure_el = await el.query_selector(self.selectors.departure)
            arrival_el = await el.query_selector(self.selectors.arrival)
            duration_el = await el.query_selector(self.selectors.duration)
            price_el = await el.query_selector(self.selectors.flight_cost)
            stop_el = await el.query_selector(self.selectors.stop)

            airline = await airline_el.inner_text()
            departure = await departure_el.inner_text()
            arrival = await arrival_el.inner_text()
            duration = await duration_el.inner_text()
            price = await price_el.inner_text()
            stop = await stop_el.inner_text()

            flights.append(
                Flight(airline, departure, arrival, duration, price, stop)
            )
            self.logger.info(f"Parsed flight: {flights[-1].to_dict()}")
        self.logger.info(f"Found {len(flights)} flights")
        return flights
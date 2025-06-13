from dataclasses import dataclass
from datetime import datetime
from logging import Logger

from domain.entities.flight import Flight
from infrastructure.browser_service import BrowserService
from infrastructure.config_browser import SelectorConfig
from infrastructure.schemas.search import FlightSearchRequest, Passenger


@dataclass
class FlightSearchUseCase:
    browser_service: BrowserService
    logger: Logger

    async def execute(self, flight_data: FlightSearchRequest) -> list[Flight]:
        async with self.browser_service as service:
            self.logger.info('Executing flight search use case')

            # Navigate to the flight search page
            await service.interactor.navigate(flight_data.url)
            # 'https://www.united.com/en/gb/fsr/choose-flights?f=LONDON&t=CHICAGO&d=2025-10-22&tt=1&sc=7&px=1,0,0,0,0,1,0,0&taxng=1&newHP=True&clm=7'
            # Choose flight type
            await self._check_flight_type(service)
            
            # Fill in the search form
            await self._fill_form(service, flight_data)

            # Submit the search form
            await service.interactor.click_element(service.selectors.search_button)

            # Parse the flight data from the results page
            flights = await service.parser.parse_flight_data()

            self.logger.info(f'Search completed with {len(flights)} flights found')
            return flights

    async def _check_flight_type(self, service: BrowserService) -> None:
        await service.client.check(service.selectors.flight_type_one)
        await service.interactor.random_delay(200, 500)

    async def _fill_form(self, service: BrowserService, flight_data: FlightSearchRequest) -> None:
        self.logger.info('Filling in the flight search form')
        selectors = service.selectors

        # Fill in the departure and arrival fields
        await service.interactor.fill_input(selectors.from_input, flight_data.departure)
        await service.interactor.fill_input(selectors.to_input, flight_data.arrival)
        
        await service.interactor.click_element('body')

        # Fill in the date fields
        if not flight_data.departure_date and not flight_data.return_date:
            self.logger.error('No departure or return date provided')
            raise ValueError('Departure or return date must be provided')
        departure_date = flight_data._formate_date(flight_data.departure_date)
        await self._fill_date(service, selectors, departure_date)
        if flight_data.return_date:
            return_date = flight_data._formate_date(flight_data.return_date)
            await self._fill_date(service, selectors, return_date)

        # Select the number of passengers
        await self._fill_passengers(service, selectors, flight_data.passengers)

        # Select the class of service
        await self._fill_service(service, selectors, flight_data.cabinType)

    async def _fill_date(
        self, 
        service: BrowserService, 
        selectors: SelectorConfig, 
        date_value: tuple[str,]
    ) -> None:
        month_name, day, year = date_value

        # open the date picker
        await service.interactor.click_element(selectors.date_input)
        await service.interactor.wait_for_element(selectors.date_modal)

        # if you need to click “next month” until you hit the right one:
        while True:
            caption = await service.interactor.inner_text(selectors.date_caption)
            if f'{month_name} {year}' in caption:
                break
            await service.interactor.click_element(selectors.next_month_btn)

        # pick the actual day cell
        try:
            day_selector = selectors.day_btn.format(day=day)
            await service.interactor.click_element(day_selector)
        except Exception as e:
            self.logger.error(f'Error selecting date {day}: {e}')
            raise ValueError(f'Could not select date {day}')    

    async def _fill_passengers(
        self, 
        service: BrowserService, 
        selectors: SelectorConfig, 
        passengers: list[Passenger]
    ) -> None:
        # open passengers dialog
        await service.interactor.click_element(selectors.passengers_field)
        await self.browser_service.interactor.wait_for_element(selectors.popup_modal)

        for passenger in passengers:
            row = await service.interactor.client.query_selector(
                selectors.passenger_row.format(category_label=passenger.category)
            )
            if row is None:
                raise RuntimeError(f"Passenger row for '{passenger.category}' not found")
            
            # Read the current value
            input_el  = await row.query_selector(selectors.caption_el)
            plus_btn  = await row.query_selector(selectors.plus_btn)
            minus_btn = await row.query_selector(selectors.minus_btn)
            
            current = int(await input_el.get_attribute("value"))
            
            while current < passenger.count:
                await plus_btn.click() 
                current = int(await input_el.get_attribute("value"))
            while current > passenger.count:
                await minus_btn.click()
                current = int(await input_el.get_attribute("value"))

        # close the dialog (if needed)
        await self.browser_service.interactor.click_element(selectors.passengers_field)

    async def _fill_service(
        self,
        service: BrowserService, 
        selectors: SelectorConfig, 
        cabinType: str
    ) -> None:
        if cabinType == 'economy':
            await self.browser_service.interactor.client.select_option(selectors.class_input, 'Economy')
        elif cabinType == 'business':
            await self.browser_service.interactor.client.select_option(selectors.class_input, 'Premium Economy')
        elif cabinType == 'first':
            await self.browser_service.interactor.client.select_option(selectors.class_input, 'Business or First')
        else:
            self.logger.warning(f'Unknown class of service: {service}')

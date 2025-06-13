from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BrowserConfig:
    """
    Configuration for the browser client.
    """
    browser_type: str = 'firefox' # 'chromium', 'firefox', or 'webkit'
    headless: bool = True # Run browser in headless mode
    proxy: Optional[str] = None 
    timeout: int = 60000 # Timeout for browser operations in milliseconds
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    custom_headers: dict = None # Custom HTTP headers to be sent with requests
    stealth_mode: bool = True # Enable stealth mode to avoid detection by anti-bot systems
    _stealth_script: str = """Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"""  

    @property
    def stealth_script(self) -> str:
        return self._stealth_script


@dataclass
class SelectorConfig:
    """
    Configuration for the selectors used in the browser client.
    """
    #Type 
    flight_type_one: str = 'input[name="flightType"][value="oneWay"]'
    
    # Navigation
    from_input: str = '#bookFlightOriginInput'
    to_input: str = '#bookFlightDestinationInput'
    
    ##Date
    date_input: str = 'button.atm-c-datepicker__icon[aria-haspopup="dialog"]'
    date_modal: str = 'div.atm-c-datepicker__modal-container[role="application"]'
    date_caption: str = 'div.rdp-month_caption .rdp-caption_label'
    next_month_btn: str = 'button.atm-c-datepicker__navigation.atm-c-datepicker-next'
    day_btn: str = 'td.rdp-day[data-day="{day}"] button.rdp-day_button'
    
    ##Passengers
    passengers_field: str = 'input.atm-c-textfield__input.atm-c-text-input--hover[type="button"]'
    popup_modal: str = 'div.atm-c-popupmodal_modal'
    passenger_row: str = 'div.app-components-PassengerSelector-passengers__passengerRow--XpEDd:has(span:has-text(\"{category_label}\"))'
    caption_el: str = 'input.atm-c-counter__input'
    plus_btn: str = 'button:has(span:has-text("Add"))'
    minus_btn: str = 'button:has(span:has-text("Subtract"))'
    
    ##Class
    class_input: str = 'select#cabinType'
    
    ##Submit
    search_button: str = 'button:has(span:has-text("Find flights"))'
    
    #Results
    result_items: str = 'div.app-components-Shopping-GridItem-styles__flightRow--QbVXL'
    flight_cost: str = 'div.app-components-Shopping-PriceCard-styles__priceValueNonUS--c6Loz:has(span)'
    airline: str = 'div.app-components-Shopping-FlightBaseCard-styles__descriptionStyle--TCjDn > div > span[aria-hidden="true"]'
    departure: str = 'span.app-components-Shopping-FlightBaseCard-styles__flightBaseCardContainer__time--DRWoI'
    arrival: str = 'span.app-components-Shopping-FlightBaseCard-styles__flightBaseCardContainer__time--DRWoI'
    duration: str = 'div.app-components-Shopping-FlightInfoBlock-styles__dividerText--Gwk7g:has(span:has-text("Duration"))'
    stop: str = 'div.app-components-Shopping-FlightBaseCard-styles__flightHeaderRight--QmZQI'

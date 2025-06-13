from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BrowserConfig:
    """
    Configuration for the browser client.
    """
    browser_type: str = 'firefox' # 'chromium', 'firefox', or 'webkit'
    headless: bool = False # Run browser in headless mode
    proxy: Optional[str] = None 
    timeout: int = 60000 # Timeout for browser operations in milliseconds
    user_agent: str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
    custom_headers: dict = field(default_factory=lambda: {
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.unted.com',
        'Priority': 'u=1, i',
        'Sec-Ch-Ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-fetch-dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        }
    )# Custom HTTP headers to be sent with requests
    stealth_mode: bool = True # Enable stealth mode to avoid detection by anti-bot systems
    _stealth_script: str = """
        () => {
            delete navigator.__proto__.webdriver;
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
                configurable: true
            });
            window.chrome = {
                runtime: {},
                app: {
                    isInstalled: false,
                    InstallState: 'disabled',
                    RunningState: 'stopped'
                }
            };
            const originalQuery = navigator.permissions.query;
            navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ? 
                Promise.resolve({ state: 'denied' }) :
                originalQuery(parameters)
            );
        }
    """

    @property
    def stealth_script(self) -> str:
        return self._stealth_script


@dataclass
class SelectorConfig:
    """
    Configuration for the selectors used in the browser client.
    """
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
    result_items: str = 'div.app-components-Shopping-FlightCard'
    flight_cost: str = 'div.app-components-Shopping-FlightCard__priceTotal'
    airline: str = 'div.app-components-Shopping-FlightCard__leg'
    departure: str = 'div.app-components-Shopping-FlightSegment__times'
    arrival: str = 'div.app-components-Shopping-FlightSegment__times'
    duration: str = 'iv.app-components-Shopping-FlightSegment__details'
    stops: str = 'div.app-components-Shopping-FlightSegment__details'

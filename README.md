# Flight Scraper

A modular web scraper that uses Playwright to extract flight information (time, price, airline, stops)

---

## Project Overview

This scraper automates a browser session against **https://www.united.com/en/gb**, fills in origin, destination, date, and passenger details, clicks “Find Flights”, then parses the first 2–3 flight cards for:

- **Departure & Arrival times**  
- **Total duration**  
- **Airline name**  
- **Price**  
- **Number of stops**

Result is printed as a JSON-style list of dictionaries.

---

## Directory Structure

flight_scraper/
├── config/
│ ├── selectors.py # all CSS/XPath selectors
│ └── browser_config.py # browser launch settings & stealth script
├── domain/
│ └── entities/
|     |-- flight.py # Flight dataclass
├── infrastructure/
| |-- schemas/
| |  |-- search.py # user request configuration
| |-- base_browser.py # abstract class
│ ├── browser_service.py # async context manager for Playwright page
│ ├── page_interactor.py # click/fill/wait helpers
│ ├── data_parser.py # scraping logic
│ ├── error_handler.py # captures screenshot + HTML on errors
│ └── browser_launcher.py # BrowserManager implements BrowserLauncher
├── application/
│ └── usecases/
│ └── search_for_flights.py # orchestrates use case
├── settings/
│ └── containers.py # Punq DI container setup
└── main.py # CLI entry point


---

## 🧩 Solution Strategy

1. **Configuration**  
   - All selectors live in `config/selectors.py`.  
   - Browser options (headless, UA, proxy, stealth) in `config/browser_config.py`.

2. **Domain Layer**  
   - `Flight` entity defined in `domain/entities.py` with fields → `to_dict()` for JSON output.

3. **Infrastructure Layer**  
   - **BrowserLauncher / BrowserManager**: abstracts Playwright startup/teardown, injects stealth script.  
   - **BrowserService**: an `async with` context that opens/closes a Playwright `Page`, provides `interactor` and `parser`.  
   - **PageInteractor**: wrappers around `page.click()`, `page.fill()`, `page.wait_for_selector()`, with randomized delays to mimic human behavior.  
   - **DataParser**: after results load, waits for spinner to disappear, then `query_selector_all` on flight cards and extracts fields.  
   - **ErrorHandler**: on any exception in the context, captures a screenshot (`error_screenshot.png`) and full-page HTML (`error_page.html`) for debugging.

4. **Application Layer**  
   - **FlightSearchUseCase**: high-level flow—open browser, handle pop-ups, fill origin/destination/date/passengers, submit, parse flights, close.

5. **Dependency Injection**  
   - `settings/containers.py` wires up all components via [Punq](https://github.com/bobthemighty/punq).  
   - Singletons for configs & logger; factories for launcher, service, use case.

---
## Running the Scraper

1. **Install dependencies**  
   ```bash
   poetry install
   playwright install

Invoke CLI
python main.py \
  --origin LON \
  --destination ORD \
  --date 22-10-2022 \
  --passenger adult - 1, child - 1 \
  --class service economy\
  --headless
Output
Prints JSON list,
[
    {
        "airline": "UA 958 (Boeing 767-300)",
        "flight_time": "08:30 - 08:30",
        "duration": "9H\nDuration 9 hours",
        "price": "\u00a31,334",
        "stop": "NONSTOP"
    },
    {
        "airline": "UA 959 (Boeing 767-300)",
        "flight_time": "11:05 - 11:05",
        "duration": "9H, 5M\nDuration 9 hours and 5 minutes",
        "price": "\u00a31,334",
        "stop": "NONSTOP"
    },
    {
        "airline": "UA 928 (Boeing 767-300)",
        "flight_time": "14:10 - 14:10",
        "duration": "9H, 10M\nDuration 9 hours and 10 minutes",
        "price": "\u00a31,334",
        "stop": "NONSTOP"
    }
]

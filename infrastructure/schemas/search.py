from dataclasses import dataclass
from datetime import datetime


@dataclass
class Passenger:
    category: str
    count: int


@dataclass
class FlightSearchRequest:
    url: str
    departure: str
    arrival: str
    departure_date: str
    passengers: list[Passenger]
    return_date: str = None
    cabinType: str = 'economy'

    def _formate_date(self, date: str) -> tuple[str, str, int]:
        """
        Format the date to 'YYYY-MM-DD' format.
        """
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            month_name = dt.strftime("%B")
            day = dt.strftime("%Y-%m-%d")
            year = dt.year
            return (month_name, day, year)
        except ValueError:
            raise ValueError("Invalid date format. Use DD-MM-YYYY")


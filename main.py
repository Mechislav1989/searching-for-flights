import asyncio
import json

from application.usecases.searches_for_flights import FlightSearchUseCase
from infrastructure.schemas.search import FlightSearchRequest, Passenger
from settings.containers import get_container


async def main() -> None:
    container = get_container()
    flight_search_uc = container.resolve(FlightSearchUseCase)
    flight_data = FlightSearchRequest(
        departure = 'New York',
        arrival = 'Los Angeles',
        departure_date = '2025-10-15',
        return_date = '2025-10-20',
        passengers = [
            Passenger(category='Adults', count=1), 
            Passenger(category='Children', count=1)
        ],
        cabinType = 'economy',
        url = 'https://www.united.com/en/gb'
    )
    flights = await flight_search_uc.execute(flight_data)
    print(flights)
    with open('flights.json', 'w') as f:
        json.dump([flight.to_dict() for flight in flights[:3]], f, indent=4)
    return flights


if __name__ == "__main__":
    asyncio.run(main())
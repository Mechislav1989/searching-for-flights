from dataclasses import dataclass


@dataclass
class Flight:
    airline: str
    arrival: str
    departure: str
    duration: str
    price: str
    stop: str
    
    def to_dict(self):
        return {
            'airline': self.airline,
            'flight_time': f'{self.departure} - {self.arrival}',
            'duration': self.duration,
            'price': self.price,
            'stop': self.stop
        }
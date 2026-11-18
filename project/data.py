TYPE_CHECKING=False
if TYPE_CHECKING:
    from typing import NewType
else:
    def NewType(_,type_):
        return type_
class datetime:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    def __init__(self, year, month, day, hour, minute):
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.minute=minute

import requests # urequests for micropython
import json
import karlskrona_stops

TransportMode = NewType('TransportMode', str)
StopID = karlskrona_stops.StopID

class DepartureInfo:
    departure_time: datetime
    line: str
    destination: str
    transport_mode: TransportMode
    departure_status: str
    def __init__(self,departure_time,line,destination,transport_mode,departure_status):
        self.departure_time=departure_time
        self.line=line
        self.destination=destination
        self.transport_mode=transport_mode
        self.departure_status=departure_status

class Data:
    stops_dict = karlskrona_stops.stops
    departures_dict: dict[StopID,tuple[DepartureInfo,...]]

    def __init__(self):
        self.departures_dict={}
        for _id in self.stops_dict:
            self.departures_dict[_id]=()

    def get_stops(self) -> tuple[StopID,...]:
        return tuple(StopID(stop_id) for stop_id in self.stops_dict.keys())

    def stop_get_name(self, stop_id: StopID) -> str:
        return self.stops_dict[stop_id]

    def stop_get_departures_info(self, current_stop: StopID) -> tuple[DepartureInfo,...]:
        return self.departures_dict.get(current_stop,())

    def get_transport_modes(self) -> tuple[TransportMode,...]:
        return (TransportMode("Bus"), TransportMode("Train"), TransportMode("Ferry"),)

    def set_departures_for_stop(self,stop: StopID,departures: tuple[DepartureInfo,...]):
        self.departures_dict[stop]=departures

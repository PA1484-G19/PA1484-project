# dataclasses and typing is missing from micropython, so in runtime mock the imported stuff
TYPE_CHECKING=False
if TYPE_CHECKING:
    from dataclasses import dataclass
    from typing import NewType
    from datetime import datetime
else:
    def dataclass(cls):
        return cls
    def NewType(_,type_):
        return type_
    @dataclass
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

class Data:
    StopID = karlskrona_stops.StopID
    TransportMode = NewType('TransportMode', str)

    @dataclass
    class DepartureInfo:
        departure_time: datetime
        line: str
        destination: Data.StopID
        transport_mode: Data.TransportMode
        departure_status: str
        def __init__(self,departure_time,line,destination,transport_mode,departure_status):
            self.departure_time=departure_time
            self.line=line
            self.destination=destination
            self.transport_mode=transport_mode
            self.departure_status=departure_status

    stops_dict = karlskrona_stops.stops

    def __init__(self):
        self.departures_dict={}
        for _id in self.stops_dict:
            self.departures_dict[_id]=[]

    def get_stops(self) -> tuple[StopID,...]:
        return tuple(self.StopID(stop_id) for stop_id in Data.stops_dict.keys())

    def stop_get_name(self, stop_id: StopID) -> str:
        return self.stops_dict.get(stop_id)

    def stop_get_departures_info(self, current_stop: StopID) -> tuple[DepartureInfo,...]:
        return self.departures_dict.get(current_stop)

    def get_transport_modes(self) -> tuple[TransportMode,...]:
        return (self.TransportMode("Bus"), self.TransportMode("Train"), self.TransportMode("Ferry"),)

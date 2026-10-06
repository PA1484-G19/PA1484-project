# dataclasses and typing is missing from micropython, so in runtime mock the imported stuff
TYPE_CHECKING=False
if TYPE_CHECKING:
    from dataclasses import dataclass
    from typing import NewType
else:
    def dataclass(cls):
        return cls
    def NewType(_,type_):
        return type_

from datetime import datetime
import requests # urequests for micropython
import json

class Data:
    StopID = NewType('StopID', int)
    TransportMode = NewType('TransportMode', str)

    @dataclass
    class DepartureInfo:
        departure_time: datetime
        line: str
        destination: Data.StopID
        transport_mode: Data.TransportMode
        departure_status: str

    #hardcoded dictionary 
    stops_dict = {
    StopID(740032188): "Campus Gräsvik",
    StopID(740000230): "Karlskrona Centralstation",
    StopID(740031781): "Bergåsa centrum",
    StopID(740000663): "Lyckeby centrum",
    StopID(740031800): "Karlskrona Amiralen",
}
    def __init__(self):
        d1 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.StopID(740000230), self.TransportMode("Bus"), "On time"
            )
        d2 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.StopID(740031781), self.TransportMode("Bus"), "Delayed"
            )
        d3 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.StopID(740000663), self.TransportMode("Train"), "On time"
            )    
        d4 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.StopID(740031800), self.TransportMode("Train"), "Delayed"
            ) 
               
        self.departures_from_campus_gräsvik = [d1, d2, d3, d4]

        d5 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.StopID(740032188), self.TransportMode("Bus"), "On time"
            )
        d6 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.StopID(740031781), self.TransportMode("Bus"), "Delayed"
            )
        d7 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.StopID(740000663), self.TransportMode("Train"), "On time"
            )    
        d8 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.StopID(740031800), self.TransportMode("Train"), "Delayed"
            ) 

        self.departures_from_karlskrona_centralstation = [d5, d6, d7, d8]

        d9 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.StopID(740032188), self.TransportMode("Bus"), "On time"
            )
        d10 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.StopID(740000230), self.TransportMode("Bus"), "Delayed"
            )
        d11 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.StopID(740000663), self.TransportMode("Train"), "On time"
            )    
        d12 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.StopID(740031800), self.TransportMode("Train"), "Delayed"
            ) 

        self.departures_from_bergåsa_centrum = [d9, d10, d11, d12]

        d13 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.StopID(740032188), self.TransportMode("Bus"), "On time"
            )
        d14 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.StopID(740000230), self.TransportMode("Bus"), "Delayed"
            )
        d15  = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.StopID(740031781), self.TransportMode("Train"), "On time"
            )    
        d16 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.StopID(740031800), self.TransportMode("Train"), "Delayed"
            )

        self.departures_from_lyckeby_centrum = [d13, d14, d15, d16]

        d17 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.StopID(740032188), self.TransportMode("Bus"), "On time"
            )
        d18 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.StopID(740000230), self.TransportMode("Bus"), "Delayed"
            )
        d19  = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.StopID(740031781), self.TransportMode("Train"), "On time"
            )    
        d20 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.StopID(740000663), self.TransportMode("Train"), "Delayed"
            )

        self.departures_from_karlskrona_amiralen = [d17, d18, d19, d20]

        self.departures_list = [
            self.departures_from_campus_gräsvik,
            self.departures_from_bergåsa_centrum,
            self.departures_from_lyckeby_centrum,
            self.departures_from_karlskrona_amiralen
        ]

        self.departures_dict = {}
        for i, stop_id in enumerate(self.stops_dict.keys()):
            self.departures_dict[stop_id] = self.departures_list[i-1]

    def get_stops(self) -> tuple[StopID,...]:
        return tuple(self.StopID(stop_id) for stop_id in Data.stops_dict.keys())

    def stop_get_name(self, stop_id: StopID) -> str:
        return self.stops_dict.get(stop_id)

    def stop_get_departures_info(self, current_stop: StopID) -> tuple[DepartureInfo,...]:
        return tuple(departure for departure in self.departures_dict.get(current_stop))

    def get_transport_modes(self) -> tuple[TransportMode,...]:
        return tuple(self.TransportMode("Bus"), self.TransportMode("Train"),)


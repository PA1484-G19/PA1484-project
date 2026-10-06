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
        def __init__(self,departure_time,line,destination,transport_mode,departure_status):
            self.departure_time=departure_time
            self.line=line
            self.destination=destination
            self.transport_mode=transport_mode
            self.departure_status=departure_status

    campus_gräsvik = StopID(740032188)
    karlskrona_centralstation = StopID(740000230)
    bergåsa_centrum = StopID(740031781)
    lyckeby_centrum = StopID(740000663)
    karlskrona_amiralen = StopID(740031800)
    #hardcoded dictionary 
    stops_dict = {
        campus_gräsvik: "Campus Gräsvik",
        karlskrona_centralstation: "Karlskrona Centralstation",
        bergåsa_centrum: "Bergåsa centrum",
        lyckeby_centrum: "Lyckeby centrum",
        karlskrona_amiralen: "Karlskrona Amiralen",
    }
    def __init__(self):
        d1 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.karlskrona_centralstation, self.TransportMode("Bus"), "On time"
            )
        d2 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.bergåsa_centrum, self.TransportMode("Bus"), "Delayed"
            )
        d3 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.lyckeby_centrum, self.TransportMode("Train"), "On time"
            )    
        d4 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.karlskrona_amiralen, self.TransportMode("Train"), "Delayed"
            ) 
               
        self.departures_from_campus_gräsvik = [d1, d2, d3, d4]

        d5 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.campus_gräsvik, self.TransportMode("Bus"), "On time"
            )
        d6 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.bergåsa_centrum, self.TransportMode("Bus"), "Delayed"
            )
        d7 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.lyckeby_centrum, self.TransportMode("Train"), "On time"
            )    
        d8 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.karlskrona_amiralen, self.TransportMode("Train"), "Delayed"
            ) 

        self.departures_from_karlskrona_centralstation = [d5, d6, d7, d8]

        d9 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.campus_gräsvik, self.TransportMode("Bus"), "On time"
            )
        d10 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.karlskrona_centralstation, self.TransportMode("Bus"), "Delayed"
            )
        d11 = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.lyckeby_centrum, self.TransportMode("Train"), "On time"
            )    
        d12 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.karlskrona_amiralen, self.TransportMode("Train"), "Delayed"
            ) 

        self.departures_from_bergåsa_centrum = [d9, d10, d11, d12]

        d13 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.campus_gräsvik, self.TransportMode("Bus"), "On time"
            )
        d14 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.karlskrona_centralstation, self.TransportMode("Bus"), "Delayed"
            )
        d15  = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.lyckeby_centrum, self.TransportMode("Train"), "On time"
            )    
        d16 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.karlskrona_amiralen, self.TransportMode("Train"), "Delayed"
            )

        self.departures_from_lyckeby_centrum = [d13, d14, d15, d16]

        d17 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 30), "Bus 1", self.campus_gräsvik, self.TransportMode("Bus"), "On time"
            )
        d18 = self.DepartureInfo(
            datetime(2026, 10, 1, 12, 45), "Bus 2", self.karlskrona_centralstation, self.TransportMode("Bus"), "Delayed"
            )
        d19  = self.DepartureInfo(
            datetime(2026, 10, 1, 15, 45), "Train 1", self.lyckeby_centrum, self.TransportMode("Train"), "On time"
            )    
        d20 = self.DepartureInfo(
            datetime(2026, 10, 1, 16, 30), "Train 2", self.karlskrona_amiralen, self.TransportMode("Train"), "Delayed"
            )

        self.departures_from_karlskrona_amiralen = [d17, d18, d19, d20]

        self.departures_dict = {
            self.karlskrona_centralstation: self.departures_from_karlskrona_centralstation,
            self.campus_gräsvik: self.departures_from_campus_gräsvik,
            self.bergåsa_centrum: self.departures_from_bergåsa_centrum,
            self.lyckeby_centrum: self.departures_from_lyckeby_centrum,
            self.karlskrona_amiralen: self.departures_from_karlskrona_amiralen
        }

    def get_stops(self) -> tuple[StopID,...]:
        return tuple(self.StopID(stop_id) for stop_id in Data.stops_dict.keys())

    def stop_get_name(self, stop_id: StopID) -> str:
        return self.stops_dict.get(stop_id)

    def stop_get_departures_info(self, current_stop: StopID) -> tuple[DepartureInfo,...]:
        return self.departures_dict.get(current_stop)

    def get_transport_modes(self) -> tuple[TransportMode,...]:
        return (self.TransportMode("Bus"), self.TransportMode("Train"),)

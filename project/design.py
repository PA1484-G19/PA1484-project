from collections.abc import Callable
from dataclasses import dataclass
from typing import NewType
from datetime import datetime

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

    def get_stops(self) -> tuple[StopID,...]:
        ...

    def stop_get_name(self, stop_id: StopID) -> str:
        ...

    def stop_get_departures_info(self) -> tuple[DepartureInfo,...]:
        ...

    def get_transport_modes(self) -> tuple[TransportMode,...]:
        ...

class SaveSystem:
    def __init__(self):
        ...

    def save(self, data: bytes):
        ...

    def load(self) -> bytes | None:
        ...

class Settings:
    def __init__(self, to_be_called_on_settings_change: Callable):
        ...

    def set_current_stop(self, stop: Data.StopID | None):
        ...

    def get_current_stop(self) -> Data.StopID | None:
        ...

    def set_current_transport_mode(self, transport: Data.TransportMode | None):
        ...

    def get_current_transport_mode(self) -> Data.TransportMode | None:
        ...

    def to_savable_format(self) -> bytes:
        ...

    def from_savable_format(self, save: bytes | None):
        ...

class TitleScreen:
    def __init__(self, tile: lv_obj_t):
        ...

class DepartureScreen:
    def __init__(self, tile: lv_obj_t, settings: Settings, data: Data):
        ...

    def settings_has_changed(self):
        ...

class SettingsScreen:
    def __init__(self, tile: lv_obj_t, data: Data, settings: Settings, savesystem: SaveSystem):
        ...

class App:
    def __init__(self):
        ...

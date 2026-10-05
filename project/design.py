from collections.abc import Callable
from dataclasses import dataclass
from typing import NewType
from datetime import datetime

#Unsure if the import should be here
import lvgl as lv


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
        # Unsure if the code fits the ESP32 screen resolution, if not some values need to be ajusted

        project_name_label = lv.label(tile)
        project_name_label.set_text("Project name: Transit go pro")
        project_name_label.align(lv.ALIGN.TOP_LEFT, 50, 50)

        version_label = lv.label(tile)
        version_label.set_text("Program version: 1.0")
        version_label.align(lv.ALIGN.TOP_LEFT, 50, 80)

        group_label = lv.label(tile)
        group_label.set_text("Group members:")
        group_label.align(lv.ALIGN.CENTER, 0, -20)

        members_text = lv.label(tile)
        members_text.align(lv.ALIGN.CENTER, 0, 10)
        members_text.set_text("Mahmoud Soufi, Tamas Dagany, Khaled Rukaia , Erik Fröjdh , Kith Ssekabira")
        members_text.set_width(350)
        members_text.set_long_mode(lv.LABEL_LONG.WRAP)


class DepartureScreen:
    def __init__(self, tile: lv_obj_t, settings: Settings, data: Data):
        # Unsure if the code fits the ES32 screen resolution, if not some values need to be ajusted
        # Unsure how the data system works so temporary data is used

        #current_stop_name = data.stop_get_name(settings.get_current_stop())
        current_stop_label = lv.label(tile)
        current_stop_label.set_text("current_stop_name")
        current_stop_label.align(lv.ALIGN.TOP_MID,0,20)


        #transport_mode = settings.get_current_transport_mode()
        transport_mode_label = lv.label(tile)
        transport_mode_label.set_text("current_transport_mode")
        transport_mode_label.align(lv.ALIGN.TOP_MID,0,45)

        list1 = lv.list(tile)
        list1.set_size(lv.pct(100), lv.pct(60))
        list1.align(lv.ALIGN.BOTTOM_MID,0,0)

        #temporary data
        for n in range(0,20):
            list1.add_text("12:31 - Destination - Line - Transport mode")





    def settings_has_changed(self):
        ...

class SettingsScreen:
    def __init__(self, tile: lv_obj_t, data: Data, settings: Settings, savesystem: SaveSystem):
        ...

class App:
    def __init__(self):
        ...

import lvgl as lv
from board_lvgl import start_board
from data import Data
from departurescreen import DepartureScreen
from fetcher import Fetcher
from savesystem import SaveSystem
from settings import Settings
from settingscreen import SettingsScreen
from titlescreen import TitleScreen


class App:
    def __init__(self):
        self.display, self.touch, self.handler = start_board()

        self.fetcher=Fetcher(lambda:self.settings.get_current_stop(),
                             lambda stop,data:(self.data.set_departures_for_stop(stop,data),
                                               self.departure_screen.settings_has_changed()))
        self.fetcher.connect()

        lv.timer_create(lambda _: self.fetcher.refetch()
                        if self.fetcher.need_refetch() else None, 2_000, None)

        self.tileview = lv.tileview(lv.screen_active())
        self.tileview.set_size(600, 450)
        self.tileview.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

        self.tile1 = self.tileview.add_tile(0, 0, lv.DIR.RIGHT)
        self.tile2 = self.tileview.add_tile(1, 0, lv.DIR.LEFT | lv.DIR.RIGHT)
        self.tile3 = self.tileview.add_tile(2, 0, lv.DIR.LEFT)

        self.data=Data()
        self.savesystem=SaveSystem()
        self.settings=Settings(lambda: self.departure_screen.settings_has_changed()
                               if not self.fetcher.need_refetch() else
                               self.fetcher.refetch())

        self.title_screen=TitleScreen(self.tile1)
        self.departure_screen=DepartureScreen(self.tile2,self.settings,self.data,self.fetcher.refetch)
        self.settings_screen=SettingsScreen(self.tile3,self.data,self.settings,self.savesystem,self.fetcher)

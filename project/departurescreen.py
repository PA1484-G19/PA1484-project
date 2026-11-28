import lvgl as lv

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable

    from data import Data
    from settings import Settings


class DepartureScreen:
    def __init__(
        self, tile: lv.obj, settings: Settings, data: Data, refresh: Callable[[], None]
    ):
        self.settings = settings
        self.data = data

        self.current_stop_label = lv.label(tile)
        self.current_stop_label.align(lv.ALIGN.TOP_MID, 0, 20)

        self.transport_mode_label = lv.label(tile)
        self.transport_mode_label.align(lv.ALIGN.TOP_MID, 0, 45)

        self.departure_list = lv.list(tile)
        self.departure_list.set_size(lv.pct(100), lv.pct(60))
        self.departure_list.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        self.refresh_btn = lv.button(tile)
        lv.label(self.refresh_btn).set_text('Refresh')
        self.refresh_btn.align(lv.ALIGN.TOP_RIGHT, -16, 16)
        self.refresh_btn.add_event_cb(lambda _event: refresh(), lv.EVENT.CLICKED, None)

        self.settings_has_changed()

    def settings_has_changed(self):
        """Re-read the settings and redraw the screen. Call this whenever
        the stop or transport mode changes."""
        stop_id = self.settings.get_current_stop()
        mode = self.settings.get_current_transport_mode()

        self.departure_list.clean()

        # Fresh start: no stop selected yet
        if stop_id is None:
            self.current_stop_label.set_text('No stop selected')
            self.transport_mode_label.set_text('')
            self.departure_list.add_text('Select a stop in Settings')
            return

        self.current_stop_label.set_text(self.data.stop_get_name(stop_id))
        self.transport_mode_label.set_text(mode if mode is not None else 'All')

        departures = self.data.stop_get_departures_info(stop_id)

        # No mode selected (or "All") means don't filter
        if mode is not None and mode != 'All':
            departures = [d for d in departures if d.transport_mode == mode]

        if not departures:
            self.departure_list.add_text('No departures')
            return

        for dep in departures:
            time_str = f'{dep.departure_time.hour:02d}:{dep.departure_time.minute:02d}'
            self.departure_list.add_text(
                f'{time_str} - {dep.destination} - {dep.line} - {dep.transport_mode} - {dep.departure_status}'
            )

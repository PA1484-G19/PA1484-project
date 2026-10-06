import lvgl as lv

# Type-only imports: MicroPython ignores annotations, so these are never run on the device
TYPE_CHECKING = False
if TYPE_CHECKING:
    from lvgl import obj as lv_obj_t
    from settings import Settings
    from data import Data


class TitleScreen:
    def __init__(self, tile: "lv_obj_t"):
        # If this doesn't fit the ESP32 screen resolution, adjust the values

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
        members_text.set_text(
            "Mahmoud Soufi, Tamas Dagany, Khaled Rukaia, Erik Fröjdh, Kith Ssekabira")
        members_text.set_width(350)
        members_text.set_long_mode(lv.LABEL_LONG.WRAP)


class DepartureScreen:
    def __init__(self, tile: "lv_obj_t", settings: "Settings", data: "Data"):
        self.settings = settings
        self.data = data

        self.current_stop_label = lv.label(tile)
        self.current_stop_label.align(lv.ALIGN.TOP_MID, 0, 20)

        self.transport_mode_label = lv.label(tile)
        self.transport_mode_label.align(lv.ALIGN.TOP_MID, 0, 45)

        self.departure_list = lv.list(tile)
        self.departure_list.set_size(lv.pct(100), lv.pct(60))
        self.departure_list.align(lv.ALIGN.BOTTOM_MID, 0, 0)

        self.settings_has_changed()

    def settings_has_changed(self):
        """Re-read the settings and redraw the screen. Call this whenever
        the stop or transport mode changes."""
        stop_id = self.settings.get_current_stop()
        mode = self.settings.get_current_transport_mode()

        self.departure_list.clean()

        # Fresh start: no stop selected yet
        if stop_id is None:
            self.current_stop_label.set_text("No stop selected")
            self.transport_mode_label.set_text("")
            self.departure_list.add_text("Select a stop in Settings")
            return

        self.current_stop_label.set_text(self.data.stop_get_name(stop_id))
        self.transport_mode_label.set_text(mode if mode else "All")

        departures = self.data.stop_get_departures_info(stop_id)

        # No mode selected (or "All") means don't filter
        if mode and mode != "All":
            departures = [d for d in departures if d.transport_mode == mode]

        if not departures:
            self.departure_list.add_text("No departures")
            return

        for dep in departures:
            time_str = "{:02d}:{:02d}".format(
                dep.departure_time.hour, dep.departure_time.minute)
            destination = self.data.stop_get_name(dep.destination)
            self.departure_list.add_text(
                "{} - {} - {} - {}".format(
                    time_str, destination, dep.line, dep.transport_mode))

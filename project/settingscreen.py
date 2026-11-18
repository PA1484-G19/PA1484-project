import lvgl as lv
import time
 
Button = getattr(lv, "button", None) or lv.btn
load_screen = getattr(lv, "screen_load", None) or lv.scr_load

STATUS_REFRESH_MS = 2000
 
 
class SettingsScreen:
    def __init__(self, tile, data, settings, savesystem, fetcher):
        self.tile = tile
        self.data = data
        self.settings = settings
        self.savesystem = savesystem
        self.fetcher = fetcher
 
        self.STOPS = data.get_stops()
        
        self.TRANSPORT_MODES = list(data.get_transport_modes()) + ["All"]
 
        
        saved = self.savesystem.load()
        if saved:
            self.settings.from_savable_format(saved)
 
        self.container = lv.obj(self.tile)
        self.container.set_size(lv.pct(90), lv.pct(90))
        self.container.center()
        self.container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
 
        title = lv.label(self.container)
        title.set_text("Settings")
 
        stop_label = lv.label(self.container)
        stop_label.set_text("Select Stop:")
        self.stop_dropdown = lv.dropdown(self.container)
        self.stop_dropdown.set_options("\n".join(map(data.stop_get_name,self.STOPS)))
        self.stop_dropdown.add_event_cb(
            self._on_stop_changed, lv.EVENT.VALUE_CHANGED, None)
 
        transport_label = lv.label(self.container)
        transport_label.set_text("Select Transport:")
        self.transport_dropdown = lv.dropdown(self.container)
        self.transport_dropdown.set_options("\n".join(self.TRANSPORT_MODES))
        self.transport_dropdown.add_event_cb(
            self._on_transport_changed, lv.EVENT.VALUE_CHANGED, None)
 
        self.save_btn = Button(self.container)
        lv.label(self.save_btn).set_text("Save as Default")
        self.save_btn.add_event_cb(
            self._on_save_clicked, lv.EVENT.CLICKED, None)
 
        self.reset_btn = Button(self.container)
        lv.label(self.reset_btn).set_text("Reset")
        self.reset_btn.add_event_cb(
            self._on_reset_clicked, lv.EVENT.CLICKED, None)

        self.wifi_status_label = lv.label(self.container)
        self.live_data_status_label = lv.label(self.container)
 
        self._sync_dropdowns()
        self._update_status()

        # LVGL 9 timer: calls _on_status_timer(timer) every STATUS_REFRESH_MS.
        # Kept on self so the timer is not garbage collected.
        self.status_timer = lv.timer_create(
            self._on_status_timer, STATUS_REFRESH_MS, None)

    def _update_status(self):
        """Show the Wi-Fi state and how old the selected stop's live data is."""
        status = self.fetcher.status()
        self.wifi_status_label.set_text(
            "Wi-Fi: Connected" if status.active else "Wi-Fi: Disconnected")

        if status.last_fetch == -1:
            self.live_data_status_label.set_text("Live data: No data yet")
        else:
            seconds = time.ticks_diff(time.ticks_ms(), status.last_fetch) // 1000
            self.live_data_status_label.set_text("Live data: %d s ago" % seconds)

    def _on_status_timer(self, timer):
        self._update_status()
 
    def _sync_dropdowns(self):
        """Set the dropdown selections so they match the current settings."""
        if self.settings.get_current_stop() in self.STOPS:
            self.stop_dropdown.set_selected(self.STOPS.index(self.settings.get_current_stop()))
 
        if self.settings.get_current_transport_mode() is None:
            self.transport_dropdown.set_selected(self.TRANSPORT_MODES.index("All"))
        elif self.settings.get_current_transport_mode() in self.TRANSPORT_MODES:
            self.transport_dropdown.set_selected(
                self.TRANSPORT_MODES.index(self.settings.get_current_transport_mode()))
 
    def _on_stop_changed(self, event):
        idx = self.stop_dropdown.get_selected()
        self.settings.set_current_stop(self.STOPS[idx])
        self._update_status()
 
    def _on_transport_changed(self, event):
        idx = self.transport_dropdown.get_selected()
        selected = self.TRANSPORT_MODES[idx]
        if selected == "All":
            self.settings.set_current_transport_mode(None)
        else:
            self.settings.set_current_transport_mode(selected)
 
    def _on_save_clicked(self, event):
        self.savesystem.save(self.settings.to_savable_format())
 
    def _on_reset_clicked(self, event):
        saved = self.savesystem.load()
        if saved:
            self.settings.from_savable_format(saved)
            self._sync_dropdowns()
            self._update_status()

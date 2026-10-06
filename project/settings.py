"""The user's selected stop and transport mode."""

import json


# Get type checking without running the import: (typing is missing from MicroPython and avoids possible
# circular imports)
TYPE_CHECKING=False
if TYPE_CHECKING:
    from typing import Callable
    from data import Data

class Settings:
    """Holds the current settings and calls a callback whenever they change."""

    def __init__(self, to_be_called_on_settings_change: "Callable"):
        self._on_change = to_be_called_on_settings_change
        self._stop = None
        self._transport_mode = None

    def set_current_stop(self, stop: "Data.StopID | None"):
        self._update(stop, self._transport_mode)

    def get_current_stop(self) -> "Data.StopID | None":
        return self._stop

    def set_current_transport_mode(self, transport: "Data.TransportMode | None"):
        self._update(self._stop, transport)

    def get_current_transport_mode(self) -> "Data.TransportMode | None":
        return self._transport_mode

    def to_savable_format(self) -> bytes:
        return json.dumps(
            {"stop": self._stop, "transport_mode": self._transport_mode}
        ).encode()

    def from_savable_format(self, save: bytes | None):
        """Restore from to_savable_format() output; None or invalid data is ignored."""
        if save is None:
            return
        try:
            record = json.loads(save.decode())
            stop = record.get("stop")
            transport = record.get("transport_mode")
        except (AttributeError, ValueError):
            return
        # StopID is an int and TransportMode a str in the agreed Data design.
        if ((stop is None or type(stop) is int) and
                (transport is None or type(transport) is str)):
            self._update(stop, transport)

    def _update(self, stop, transport):
        # Notify only on a real change, so screens are not refreshed needlessly.
        if stop != self._stop or transport != self._transport_mode:
            self._stop = stop
            self._transport_mode = transport
            self._on_change()

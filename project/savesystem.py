"""Non-volatile storage for the serialized settings."""

from debug_log import log


# A file on the board's FAT flash filesystem, beside main.py. It survives
# reboots and power loss; flashing the Python application again resets it.
SAVE_PATH = "/settings.dat"


class SaveSystem:
    """Stores one blob of bytes in a file on the board's flash."""

    def __init__(self):
        self.path = SAVE_PATH

    def save(self, data: bytes):
        try:
            with open(self.path, "wb") as stream:
                stream.write(data)
        except OSError as error:
            log("SaveSystem: could not save settings: %r" % (error,))

    def load(self) -> bytes | None:
        """Return the saved bytes, or None if nothing has been saved yet."""
        try:
            with open(self.path, "rb") as stream:
                return stream.read()
        except OSError:
            return None

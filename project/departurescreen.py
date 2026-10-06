import lvgl as lv

# Type-only imports: MicroPython ignores annotations, so these are never run on the device
TYPE_CHECKING = False
if TYPE_CHECKING:
    from lvgl import obj as lv_obj_t


class TitleScreen:
    def __init__(self, tile: lv_obj_t):
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

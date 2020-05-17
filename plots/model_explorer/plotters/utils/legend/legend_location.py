from enum import Enum


class LegendLocation(Enum):
    NONE = "None"
    top_left = "Top Left"
    top_center = "Top Center"
    top_right = "Top Right"
    center_left = "Center Left"
    center = "Center"
    center_right = "Center Right"
    bottom_left = "Bottom Left"
    bottom_center = "Bottom Center"
    bottom_right = "Bottom Right"

    @classmethod
    def options(self) -> list:
        return [(option.name, option.value) for option in self]

from enum import Enum


class VerticalAlignment(Enum):
    top = "Top"
    middle = "Middle"
    bottom = "Bottom"
    alphabetic = "Alphabetic"
    hanging = "Hanging"

    @classmethod
    def options(self) -> list:
        return [(option.name, option.value) for option in self]

from enum import Enum


class Orientation(Enum):
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"

    @classmethod
    def options(self) -> list:
        return [(option.name, option.value) for option in self]

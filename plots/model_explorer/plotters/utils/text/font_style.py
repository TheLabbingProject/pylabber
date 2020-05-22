from enum import Enum


class FontStyle(Enum):
    normal = "Normal"
    italic = "Italic"
    bold = "Bold"
    bold_italic = "Bold+Italic"

    @classmethod
    def options(self) -> list:
        return [(option.name.replace("_", " "), option.value) for option in self]

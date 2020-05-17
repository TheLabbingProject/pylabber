from enum import Enum


class Font(Enum):
    arial = "Arial"
    calibri = "Calibri"
    cursive = "Cursive"
    fantasy = "Fantasy"
    georgia = "Georgia"
    helvetica = "Helvetica"
    monospace = "Monospace"
    sans_serif = "Sans-Serif"
    serif = "Serif"
    system_ui = "System UI"
    times = "Times"
    verdana = "Verdana"

    @classmethod
    def options(self) -> list:
        return [(option.name.replace("_", "-"), option.value) for option in self]

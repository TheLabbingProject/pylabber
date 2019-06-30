from bokeh.palettes import (
    Spectral11,
    Greys256,
    Inferno256,
    Magma256,
    Plasma256,
    Viridis256,
    Cividis256,
    Purples9,
    Blues9,
    Greens9,
    Oranges9,
    Reds9,
    Colorblind8,
)

DEFAULT_PALETTE = 'Spectral'

palette_dict = {
    'Spectral': Spectral11,
    'Greys': Greys256,
    'Inferno': Inferno256,
    'Magma': Magma256,
    'Plasma': Plasma256,
    'Viridis': Viridis256,
    'Cividis': Cividis256,
    'Purples': Purples9,
    'Blues': Blues9,
    'Greens': Greens9,
    'Oranges': Oranges9,
    'Reds': Reds9,
    'Color Blind': Colorblind8,
}


def get_default_palette():
    return palette_dict[DEFAULT_PALETTE]
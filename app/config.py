import flet as ft


__all__ = [
    'header_properties',
    'textfield_properties',
    'text_properties',
    'small_text_properties',
    'boxshadow_properties',
]


header_properties = {
    'size': 35,
    'weight': ft.FontWeight.W_700,
}

text_properties = {
    'size': 20,
    'weight': ft.FontWeight.W_400,
}

small_text_properties = {
    'size': 15,
    'weight': ft.FontWeight.W_400,
}

textfield_properties = {
    # 'dense': True
}

boxshadow_properties = {
    'spread_radius': 100,
    'blur_radius': 1000,
    'color': ft.colors.BLACK,
    'blur_style': ft.ShadowBlurStyle.NORMAL,
}
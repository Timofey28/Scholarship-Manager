import flet as ft

from app.config import *


__all__ = [
    'HeaderText',
    'Text',
    'TextField',
]


class HeaderText(ft.Text):
    def __init__(self, label: str, **kwargs):
        for prop in header_properties:
            if prop not in kwargs:
                kwargs[prop] = header_properties[prop]
        super().__init__(label, **kwargs)


class Text(ft.Text):
    def __init__(self, label: str, **kwargs):
        for prop in text_properties:
            if prop not in kwargs:
                kwargs[prop] = text_properties[prop]
        super().__init__(label, **kwargs)


class TextField(ft.TextField):
    def __init__(self, label: str, **kwargs):
        for prop in textfield_properties:
            if prop not in kwargs:
                kwargs[prop] = textfield_properties[prop]
        super().__init__(label=label, **kwargs)
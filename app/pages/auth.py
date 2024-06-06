import flet as ft
from flet_core.control_event import ControlEvent
import logging

from app.custom_controls import *


class Auth:
    def __init__(self, page: ft.Page, submit_function):
        self.page = page
        self.submit_function = submit_function

        self.input_login = None
        self.input_password = None
        self.button_submit = None


    def load_page(self) -> None:
        self.input_login = TextField(label='Логин', on_change=self.__validate)
        self.input_password = TextField(label='Пароль', password=True, can_reveal_password=True, on_change=self.__validate)
        self.button_submit = ft.ElevatedButton(text='Войти', disabled=True, on_click=self.submit_function)

        self.page.clean()
        self.page.title = 'Авторизация'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.add(
            ft.Row(
                controls=[
                    ft.Column([
                        self.input_login,
                        self.input_password,
                        self.button_submit
                    ])
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )


    def __validate(self, e: ControlEvent) -> None:
        if all([self.input_login.value, self.input_password.value]):
            self.button_submit.disabled = False
        else:
            self.button_submit.disabled = True
        self.page.update()
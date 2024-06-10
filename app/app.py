import os
import json
import flet as ft
from flet_core.control_event import ControlEvent
import logging

from data import db_dbname, db_host, db_user, db_password
from database import Database
from app.pages import Auth
from app.pages import Menu


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = Database(
            db_dbname=db_dbname,
            db_host=db_host,
            db_user=db_user,
            db_password=db_password
        )
        self.page.theme_mode = ft.ThemeMode.DARK
        self.auth = None
        self.menu = None
        self.menu_specific_strategy = None

        logging.debug('Initialized App object')


    def run(self):
        self.auth = Auth(self.page, self.button_auth_submit)
        self.menu = Menu(self.page, self.db, self.button_menu_logout)

        self.auth.load_page()
        # self.menu.load_page(1)  # debug mode


    def button_auth_submit(self, e: ControlEvent):
        login = self.auth.input_login.value.strip()
        password = self.auth.input_password.value
        employee_id = self.db.login_employee(login, password)
        if employee_id:
            self.menu.load_page(employee_id)
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Неверный логин или пароль'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()


    def button_menu_logout(self):
        self.auth.load_page()
import flet as ft
from flet import ControlEvent
import logging

from database import Database
from app.custom_controls import *
from app.pages.edit_student_options.general_info import GeneralInfo
from app.pages.edit_student_options.grades import Grades
from app.pages.edit_student_options.payment_method import PaymentMethod
from app.pages.edit_student_options.penalties import Penalties


class EditStudent:
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function):
        self.page = page
        self.db = db
        self.student_id = student_id
        self.out_function = out_function
        self.page.title = 'Редактирование данных студента'

        self.editing_option = None


    def load_page(self):
        header = HeaderText('Редактирование данных студента')
        question = Text('Какие данные вы хотите изменить?')
        button_back = ft.Chip(label=ft.Text('Назад'), leading=ft.Icon(ft.icons.KEYBOARD_RETURN), on_click=lambda _: self.out_function())

        containers_bgcolor = ft.colors.GREY_900 if self.page.theme_mode == ft.ThemeMode.DARK else ft.colors.GREY_300
        cont_general_info = ft.Container(
            content=Text('Общие данные\nстудента'),
            data='general_info',
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=containers_bgcolor,
            width=230,
            height=230,
            border_radius=10,
            ink=True,
            on_click=self.__load_desired_page,
        )
        cont_grades = ft.Container(
            content=Text('Оценки'),
            data='grades',
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=containers_bgcolor,
            width=230,
            height=230,
            border_radius=10,
            ink=True,
            on_click=self.__load_desired_page,
        )
        cont_payment_method = ft.Container(
            content=Text('Способ выплаты\nстипендии'),
            data='payment_method',
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=containers_bgcolor,
            width=230,
            height=230,
            border_radius=10,
            ink=True,
            on_click=self.__load_desired_page,
        )
        cont_penalties = ft.Container(
            content=Text('Вычеты и штрафы'),
            data='penalties',
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=containers_bgcolor,
            width=230,
            height=230,
            border_radius=10,
            ink=True,
            on_click=self.__load_desired_page,
        )

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([question], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                controls=[
                    cont_general_info,
                    cont_grades,
                    cont_payment_method,
                    cont_penalties
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row([button_back], alignment=ft.MainAxisAlignment.CENTER),
        )


    def __load_desired_page(self, e: ControlEvent):
        data = e.control.data
        if data == 'general_info':
            self.editing_option = GeneralInfo(self.page, self.db, self.student_id, self.out_function, self.load_page)
        elif data == 'grades':
            self.editing_option = Grades(self.page, self.db, self.student_id, self.out_function, self.load_page)
        elif data == 'payment_method':
            self.editing_option = PaymentMethod(self.page, self.db, self.student_id, self.out_function, self.load_page)
        elif data == 'penalties':
            self.editing_option = Penalties(self.page, self.db, self.student_id, self.out_function, self.load_page)
        else:
            logging.error('Unknown editing option')
            return

        self.editing_option.load_editing_page()
import flet as ft
from flet import ControlEvent
import logging

from database import Database
from app.custom_controls import *


class OrderCreator:
    def __init__(self, page: ft.Page, db: Database, out_function):
        self.page = page
        self.db = db
        self.out_function = out_function
        self.page.title = 'Создание приказа'
        self.institute_numbers = self.db.get_unique_institute_numbers()
        self.groups = self.db.get_groups()
        self.students = self.db.get_students()

        self.INSTITUTE = 'institute'
        self.GROUP = 'group'
        self.STUDENT = 'student'

        # Controls
        self.cr_order_number = None
        self.cr_scope_dropdown = None
        self.search_bar = None
        self.cr_enrollment_amount = None
        self.button_back = None
        self.button_create = None


    def load_page(self) -> None:
        header = HeaderText('Создание приказа')
        self.cr_order_number = TextField('Номер приказа', width=300, on_change=self.__validate_fields)
        self.cr_scope_dropdown = ft.Dropdown(
            width=300,
            options=[
                ft.dropdown.Option(text='Институт', key=self.INSTITUTE),
                ft.dropdown.Option(text='Группа', key=self.GROUP),
                ft.dropdown.Option(text='Студент', key=self.STUDENT),
            ],
            on_change=self.__change_visibility,
        )
        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='',
            view_hint_text='',
            controls=[],
            width=500,
            visible=False,
            data=None,
            on_change=self.__validate_fields,
        )
        self.cr_enrollment_amount = TextField('Сумма зачисления', width=300, on_change=self.__validate_fields)

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.out_function())
        self.button_create = ft.ElevatedButton('Создать', disabled=True, on_click=self.__create_order)

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=self.cr_order_number, margin=ft.margin.only(left=200, top=20)),
            ft.Container(content=self.cr_scope_dropdown, margin=ft.margin.only(left=200, top=15)),
            ft.Container(content=self.search_bar, margin=ft.margin.only(left=200, top=15)),
            ft.Container(content=self.cr_enrollment_amount, margin=ft.margin.only(left=200, top=15)),
            ft.Container(
                content=ft.Row([
                    self.button_back,
                    self.button_create,
                ]),
                margin=ft.margin.only(left=200, top=20),
            ),
        )


    def __change_visibility(self, e: ControlEvent) -> None:
        def close_anchor(ee: ControlEvent) -> None:
            self.search_bar.close_view(ee.control.title.value)
            self.search_bar.data = ee.control.data
            self.__validate_fields(ee)
            self.page.update()

        self.search_bar.visible = True
        self.search_bar.close_view()  # не работает, но и ошибку не выдает сучка
        if self.cr_scope_dropdown.value == self.INSTITUTE:
            self.search_bar.bar_hint_text = 'Выберите институт'
            self.search_bar.view_hint_text = 'Выберите институт...'
            self.search_bar.controls = [
                ft.ListTile(
                    title=Text(str(institute_number)),
                    data=institute_number,
                    on_click=close_anchor,
                ) for institute_number in self.institute_numbers
            ]
        elif self.cr_scope_dropdown.value == self.GROUP:
            self.search_bar.bar_hint_text = 'Выберите группу'
            self.search_bar.view_hint_text = 'Выберите группу...'
            self.search_bar.controls = [
                ft.ListTile(
                    title=Text(group['name']),
                    data=group['id'],
                    on_click=close_anchor,
                ) for group in self.groups
            ]
        elif self.cr_scope_dropdown.value == self.STUDENT:
            self.search_bar.bar_hint_text = 'Выберите студента'
            self.search_bar.view_hint_text = 'Выберите студента...'
            self.search_bar.controls = [
                ft.ListTile(
                    title=Text(student['fio']),
                    data=student['id'],
                    on_click=close_anchor,
                ) for student in self.students
            ]
        else:
            self.search_bar.visible = False
        self.__validate_fields(e)
        self.page.update()


    def __validate_fields(self, e: ControlEvent) -> None:
        if all([
            self.cr_order_number.value,
            self.cr_scope_dropdown.value,
            self.search_bar.value,
            self.cr_enrollment_amount.value,
        ]):
            if self.cr_order_number.value.isnumeric() and int(self.cr_order_number.value) > 0 and \
                    self.cr_enrollment_amount.value.isnumeric() and int(self.cr_enrollment_amount.value) > 0:
                self.button_create.disabled = False
            else:
                self.button_create.disabled = True
        else:
            self.button_create.disabled = True
        self.page.update()


    def __create_order(self, e: ControlEvent) -> None:
        number = int(self.cr_order_number.value)
        enrollment_amount = int(self.cr_enrollment_amount.value)
        scope = self.cr_scope_dropdown.value
        some_id = self.search_bar.data

        intsitute_number = None
        group_id = None
        student_id = None

        if scope == self.INSTITUTE:
            intsitute_number = some_id
        elif scope == self.GROUP:
            group_id = some_id
        elif scope == self.STUDENT:
            student_id = some_id
        else:
            logging.error('Unknown scope')
            return

        try:
            self.db.create_order(number, scope, intsitute_number, group_id, student_id, enrollment_amount)
        except:
            self.db.cur.execute('ROLLBACK;')
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Уже существует приказ с таким номером'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.page.snack_bar = ft.SnackBar(content=ft.Text('Приказ успешно создан!'), show_close_icon=True)
        self.page.snack_bar.open = True
        self.page.update()
        self.out_function()
import logging
from time import sleep
import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from .edit_student import EditStudent
from .add_student import AddStudent
from .create_order import OrderCreator
from .calculate_scholarship import ScholarshipCalculator


class Menu:
    def __init__(self, page: ft.Page, db: Database, logout_function):
        self.page = page
        self.db = db
        self.logout_function = logout_function
        self.employee_id = None
        self.button_open_drawer = None


    def load_page(self, employee_id: int):
        self.employee_id = employee_id
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        def show_drawer(e: ControlEvent) -> None:
            self.page.end_drawer.open = True
            self.page.update()

        self.page.end_drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label='Выход',
                    icon=ft.icons.LOGOUT_OUTLINED,
                    selected_icon=ft.icons.LOGOUT,
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label='Студенты',
                    icon=ft.icons.EMOJI_PEOPLE_OUTLINED,
                    selected_icon=ft.icons.EMOJI_PEOPLE,
                ),
                ft.NavigationDrawerDestination(
                    label='Приказы',
                    icon=ft.icons.MAIL_OUTLINED,
                    selected_icon=ft.icons.MAIL,
                ),
                ft.NavigationDrawerDestination(
                    label='Настройки',
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon=ft.icons.SETTINGS,
                ),
            ],
            on_change=self.change_section
        )
        if employee_id == 1:
            self.page.end_drawer.controls.insert(5, ft.NavigationDrawerDestination(
                label='Сотрудники',
                icon=ft.icons.PEOPLE_OUTLINED,
                selected_icon=ft.icons.PEOPLE,
            ))
        self.page.end_drawer.selected_index = 1

        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.MENU_OPEN,
            tooltip='Открыть меню',
            mouse_cursor=ft.MouseCursor.CLICK,
            on_click=show_drawer
        )

        self.page.title = 'Меню'
        self.build_section_students()


    def change_section(self, e: ControlEvent):
        self.page.end_drawer.open = False
        self.page.update()
        match self.page.end_drawer.selected_index:
            case 0:
                self.page.end_drawer = None
                self.page.floating_action_button = None
                self.page.theme_mode = ft.ThemeMode.DARK
                self.logout_function()
            case 1: self.build_section_students()
            case 2: self.build_section_orders()
            case 3:
                if self.employee_id == 1:
                    self.build_section_employees()
                else:
                    self.build_section_settings()
            case 4: self.build_section_settings()
            case _: self.build_section_students()


    def build_section_students(self) -> None:
        def add_student_window(e: ControlEvent):
            add_student = AddStudent(self.page, self.db, self.build_section_students)
            add_student.load_page()

        def edit_student_window(e: ControlEvent):
            search_bar.close_view('')
            sleep(0.1)
            student_id = e.control.data
            edit_student = EditStudent(self.page, self.db, student_id, self.build_section_students)
            edit_student.load_page()

        def calculate_scholarships_window(e: ControlEvent):
            scholarship_calculator = ScholarshipCalculator(self.page, self.db, self.build_section_students)
            scholarship_calculator.load_page()

        students = self.db.get_students()
        header = HeaderText('Студенты')
        search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='Поиск по студентам',
            view_hint_text='Введите ФИО студента...',
            controls=[
                ft.ListTile(
                    title=ft.Text(student['fio']),
                    data=student['id'],
                    on_click=edit_student_window,
                ) for student in students
            ],
            width=500
        )
        button_add_student = ft.ElevatedButton(
            'Добавить студента',
            icon=ft.icons.ADD,
            on_click=add_student_window,
        )
        button_calculate_scholarships = ft.Chip(
            label=Text('Рассчитать стипендии'),
            leading=ft.Icon(ft.icons.CALCULATE),
            on_click=calculate_scholarships_window,
        )

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([search_bar, button_add_student], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([button_calculate_scholarships], alignment=ft.MainAxisAlignment.CENTER),
        )


    def build_section_orders(self) -> None:
        def create_order_window(e: ControlEvent) -> None:
            order_creator = OrderCreator(self.page, self.db, self.build_section_orders)
            order_creator.load_page()

        def delete_order(e: ControlEvent) -> None:
            def cancel(ee: ControlEvent):
                self.page.overlay.clear()
                self.page.update()

            def delete(ee: ControlEvent):
                self.db.delete_order(e.control.data)
                self.page.overlay.clear()
                self.build_section_orders()

            confirmation = Text('Вы уверены, что хотите удалить приказ?')
            no = ft.ElevatedButton('Нет', on_click=cancel)
            yes = ft.ElevatedButton('Да', on_click=delete)
            content = ft.Container(
                content=ft.Column([confirmation, no, yes]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20),
                width=500,
                height=180,
                bgcolor=ft.colors.BLUE_GREY_600,
                border_radius=20,
                shadow=BoxShadow(),
            )
            self.page.overlay.append(
                ft.Row(
                    [ft.Column([content], alignment=ft.MainAxisAlignment.CENTER)],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            self.page.update()

        header = HeaderText('Приказы')
        button_create_order = ft.Chip(
            label=Text('Создать приказ'),
            leading=ft.Icon(ft.icons.ADD),
            on_click=create_order_window,
        )
        orders = self.db.get_orders()
        orders_phrase = Text('Приказы:', visible=True if orders else False)
        order_list = ft.ListView(expand=1, width=800, spacing=10)
        scope2humanview = {
            'institute': 'институт',
            'group': 'группа',
            'student': 'студент',
        }
        groups: dict = {group['id']: group['name'] for group in self.db.get_groups()}
        students: dict = {student['id']: student['fio'] for student in self.db.get_students()}
        for order in orders:
            subject = ''
            if order['scope'] == 'institute':
                subject = order['institute_number']
            elif order['scope'] == 'group':
                subject = groups[order['group_id']]
            elif order['scope'] == 'student':
                subject = students[order['student_id']]
            else:
                logging.error(f'Unknown scope: {order["scope"]}')
            amount = f"{order['enrollment_amount']:_}".replace('_', '.') + ',00 ₽'
            order_date = order['date'].strftime('%d.%m.%Y')
            order_list.controls.append(
                ft.ListTile(
                    title=Text(f"Приказ {order['number']}"),
                    subtitle=SmallText(f"Дата формирования: {order_date}\nМасштаб распространения: {subject} ({scope2humanview[order['scope']]})\nСумма: {amount}"),
                    leading=ft.Container(content=ft.Icon(ft.icons.MAIL), alignment=ft.alignment.top_center, width=50, margin=ft.margin.only(top=-20)),
                    trailing=ft.IconButton(ft.icons.DELETE, tooltip='Удалить приказ', data=order['id'], on_click=delete_order),
                    bgcolor=ft.colors.BLUE_900,
                )
            )

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=button_create_order, margin=ft.margin.only(left=200, top=20)),
            ft.Container(content=orders_phrase, margin=ft.margin.only(left=200, top=15)),
            ft.Container(content=order_list, width=800, margin=ft.margin.only(left=200, top=15)),
        )


    def build_section_employees(self) -> None:
        def create_account(e: ControlEvent):
            def validate(ee: ControlEvent):
                if login.value and password.value:
                    button_create.disabled = False
                else:
                    button_create.disabled = True
                self.page.update()

            def cancel(ee: ControlEvent):
                self.page.overlay.clear()
                self.page.update()

            def create(ee: ControlEvent):
                self.db.create_employee(login.value, password.value)
                self.page.overlay.clear()
                self.build_section_employees()

            login = TextField('Логин', width=500, on_change=validate)
            password = TextField('Пароль', width=500, on_change=validate)
            button_calcel = ft.ElevatedButton('Отмена', on_click=cancel)
            button_create = ft.ElevatedButton('Создать', disabled=True, on_click=create)
            content = ft.Container(
                content=ft.Column([login, password, button_calcel, button_create]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20),
                width=600,
                height=250,
                bgcolor=ft.colors.BLUE_GREY_600,
                border_radius=20,
                shadow=ft.BoxShadow(
                    spread_radius=0.0,
                    blur_radius=0.0,
                    color=ft.colors.BLACK,
                    blur_style=ft.ShadowBlurStyle.NORMAL
                )
            )
            self.page.overlay.append(
                ft.Row(
                    [ft.Column([content], alignment=ft.MainAxisAlignment.CENTER)],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            self.page.update()

        def delete_account(e: ControlEvent):
            def cancel(ee: ControlEvent):
                self.page.overlay.clear()
                self.page.update()

            def delete(ee: ControlEvent):
                self.db.delete_employee(e.control.data)
                self.page.overlay.clear()
                self.build_section_employees()

            confirmation = Text('Вы уверены, что хотите удалить аккаунт?')
            no = ft.ElevatedButton('Нет', on_click=cancel)
            yes = ft.ElevatedButton('Да', on_click=delete)
            content = ft.Container(
                content=ft.Column([confirmation, no, yes]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20),
                width=500,
                height=180,
                bgcolor=ft.colors.BLUE_GREY_600,
                border_radius=20,
                shadow=BoxShadow(),
            )
            self.page.overlay.append(
                ft.Row(
                    [ft.Column([content], alignment=ft.MainAxisAlignment.CENTER)],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
            self.page.update()

        header = HeaderText('Сотрудники')
        button_create_account = ft.Chip(
            label=Text('Создать аккаунт'),
            leading=ft.Icon(ft.icons.PERSON_ADD),
            on_click=create_account,
        )
        employees = self.db.get_employees()
        employees_accounts_phrase = Text('Аккаунты сотрудников:', visible=True if employees else False)
        employees_accounts = ft.ListView(
            controls=[
                ft.ListTile(
                    title=ft.Text(employee),
                    leading=ft.Icon(ft.icons.PERSON),
                    trailing=ft.IconButton(ft.icons.DELETE, data=employee, tooltip='Удалить аккаунт', on_click=delete_account),
                    bgcolor=ft.colors.BLUE_900,
                ) for employee in employees
            ],
            expand=1,
            width=500,
            spacing=10,
        )

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=button_create_account, margin=ft.margin.only(left=200, top=20)),
            ft.Container(content=employees_accounts_phrase, margin=ft.margin.only(left=200, top=15)),
            ft.Container(content=employees_accounts, width=500, margin=ft.margin.only(left=200, top=15)),
        )


    def build_section_settings(self) -> None:
        header = HeaderText('Настройки')

        def change_theme(e: ControlEvent):
            nonlocal button_theme_icon
            if self.page.theme_mode == ft.ThemeMode.LIGHT:
                self.page.theme_mode = ft.ThemeMode.DARK
                button_theme_icon.icon = ft.icons.NIGHTLIGHT
            else:
                self.page.theme_mode = ft.ThemeMode.LIGHT
                button_theme_icon.icon = ft.icons.LIGHT_MODE
            self.page.update()

        button_theme_icon = ft.IconButton(ft.icons.LIGHT_MODE, tooltip='Сменить тему', on_click=change_theme)
        if self.page.theme_mode == ft.ThemeMode.DARK:
            button_theme_icon.icon = ft.icons.NIGHTLIGHT
        app_theme = ft.Row(controls=[Text('Тема приложения'), button_theme_icon])

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([app_theme], width=self.page.width/2, alignment=ft.MainAxisAlignment.CENTER),
        )
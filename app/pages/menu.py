from time import sleep
import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from .edit_student import EditStudent
from .add_student import AddStudent


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
        # self.page.vertical_alignment = ft.MainAxisAlignment.START
        # self.page.add(
        #     ft.Row(
        #         controls=[
        #             ft.Text('Поздравляю, ты во мне!')
        #             # ft.Column([
        #             #     ft.Text('Поздравляю, ты во мне!')
        #             # ])
        #         ],
        #         alignment=ft.MainAxisAlignment.CENTER
        #     ),
        # )
        self.build_section_students()


    def change_section(self, e: ControlEvent):
        self.page.end_drawer.open = False
        self.page.update()
        match self.page.end_drawer.selected_index:
            case 0:
                self.page.end_drawer = None
                self.page.floating_action_button = None
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
        students = self.db.get_students()

        def close_anchor(e: ControlEvent):
            search_bar.close_view()
            sleep(0.1)
            # todo: вызвать метод загрузки страницы из класса EditStudent

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
                    on_click=close_anchor,
                ) for student in students
            ],
            width=500
        )
        button_add_student = ft.ElevatedButton(
            'Добавить студента',
            icon=ft.icons.ADD,
            on_click=self.__add_student_window,
        )

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([search_bar, button_add_student], alignment=ft.MainAxisAlignment.CENTER),
        )


    def __add_student_window(self, e: ControlEvent):
        add_student = AddStudent(self.page, self.db, self.build_section_students)
        add_student.load_page()


    def build_section_orders(self) -> None:
        header = HeaderText('Приказы')

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
        )


    def build_section_employees(self) -> None:
        header = HeaderText('Сотрудники')

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
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
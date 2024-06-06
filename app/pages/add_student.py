import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *


class AddStudent:
    def __init__(self, page: ft.Page, db: Database, out_function):
        self.page = page
        self.db = db
        self.out_function = out_function
        self.page.title = 'Добавление студента'

        self.groups = None
        self.selected_group_id = None
        self.selected_direction_id = None
        self.selected_support_category_id = None

        # Controls
        self.surname = None
        self.name = None
        self.patronymic = None
        self.passport_serie = None
        self.passport_number = None
        self.address = None
        self.institute_number = None
        self.group = self.group_adder = self.group_input_field = self.button_group_adder = None
        self.course = None
        self.direction = None
        self.reason_text = self.reason_switch = self.reason_textfield = None
        self.union_member_text = self.union_member_switch = None
        self.support_category = None
        self.button_back = None
        self.button_add_student = None


    def load_page(self):
        self.groups = self.db.get_groups()

        def close_anchor_direction(e: ControlEvent) -> None:
            direction_data = e.control.data
            self.selected_direction_id = direction_data['id']
            self.direction.close_view(f"{direction_data['code']}, {direction_data['name']}")
            self.__validate_fields(e)
            self.page.update()

        def close_anchor_support_category(e: ControlEvent) -> None:
            self.selected_support_category_id = e.control.data['id']
            self.support_category.close_view(e.control.data['name'])
            self.__validate_fields(e)
            self.page.update()

        header = HeaderText('Добавление студента')

        self.surname = TextField('Фамилия', on_change=self.__validate_fields)
        self.name = TextField('Имя', on_change=self.__validate_fields)
        self.patronymic = TextField('Отчество', on_change=self.__validate_fields)
        self.passport_serie = TextField('Серия паспорта', on_change=self.__validate_fields)
        self.passport_number = TextField('Номер паспорта', on_change=self.__validate_fields)
        self.address = TextField('Адрес', on_change=self.__validate_fields, width=1000)
        self.institute_number = TextField('Номер института', on_change=self.__validate_fields)

        self.group = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='Группа',
            view_hint_text='Введите номер группы...',
            controls=[
                ft.ListTile(
                    title=ft.Text(group['name']),
                    data=group,
                    on_click=self.__close_anchor_group,
                ) for group in self.groups
            ],
            on_change=self.__validate_fields,
            width=300,
        )
        self.group_adder = ft.IconButton(icon=ft.icons.ADD_CIRCLE, tooltip='Добавить группу', on_click=self.__enter_group)
        self.group_input_field = TextField('Новая группа', visible=False, on_change=self.__validate_group_input_field)
        self.button_group_adder = ft.OutlinedButton('Добавить', visible=False, disabled=True, on_click=self.__add_group)

        self.course = TextField('Курс', on_change=self.__validate_fields)
        self.direction = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='Направление',
            view_hint_text='Выберите направление обучения...',
            controls=[
                ft.ListTile(
                    title=ft.Text(direction['name']),
                    subtitle=ft.Text(direction['code']),
                    data=direction,
                    on_click=close_anchor_direction,
                ) for direction in self.db.get_directions()
            ],
            on_change=self.__validate_fields,
            width=1000,
        )

        self.reason_text = Text('Имеет право получать стипендию?')
        self.reason_switch = ft.Switch(value=True, on_change=self.__process_reason_switch)
        self.reason_textfield = TextField('Почему не имеет?', visible=False, on_change=self.__validate_fields)

        self.union_member_text = Text('Член профсоюза?')
        self.union_member_switch = ft.Switch(value=False)
        self.support_category = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='Категория поддержки',
            view_hint_text='Выберите категорию поддержки...',
            controls=[
                ft.ListTile(
                    title=ft.Text(category['name']),
                    data=category,
                    on_click=close_anchor_support_category,
                ) for category in self.db.get_support_categories()
            ],
            width=500,
        )
        self.support_category.value = 'Нет'
        self.selected_support_category_id = 1

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.out_function())
        self.button_add_student = ft.ElevatedButton('Добавить студента', disabled=True, on_click=self.__add_student)

        self.page.clean()
        self.page.add(ft.ListView(
            controls=[
                ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.surname], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.name], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.patronymic], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.passport_serie, self.passport_number], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.address], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.institute_number], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.group, self.group_adder, self.group_input_field, self.button_group_adder], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.course], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.direction], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.reason_text, self.reason_switch, self.reason_textfield], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.union_member_text, self.union_member_switch], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Text('Категория материальной поддержки:'), self.support_category], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.button_back, self.button_add_student], alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=1,
            spacing=20,
            padding=10,
        ))

    def __close_anchor_group(self, e: ControlEvent) -> None:
        self.selected_group_id = e.control.data['id']
        self.group.close_view(e.control.data['name'])
        self.__validate_fields(e)
        self.page.update()


    def __enter_group(self, e: ControlEvent) -> None:
        if self.group_input_field.visible:
            self.group_adder.icon = ft.icons.ADD_CIRCLE
            self.group_adder.tooltip = 'Добавить группу'
            self.group_input_field.visible = False
            self.button_group_adder.visible = False
        else:
            self.group_adder.icon = ft.icons.REMOVE_CIRCLE
            self.group_adder.tooltip = 'Отменить добавление'
            self.group_input_field.visible = True
            self.button_group_adder.visible = True
            self.group_input_field.value = ''
        self.page.update()


    def __add_group(self, e: ControlEvent) -> None:
        if self.group_input_field.value in list(map(lambda x: x['name'], self.groups)):
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f'Группа {self.group_input_field.value} уже существует'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.group_adder.icon = ft.icons.ADD_CIRCLE
        self.group_adder.tooltip = 'Добавить группу'
        self.group_input_field.visible = False
        self.button_group_adder.visible = False
        self.db.add_group(self.group_input_field.value)
        self.group.value = self.group_input_field.value
        self.groups = self.db.get_groups()
        self.group.controls = [
            ft.ListTile(
                title=ft.Text(group['name']),
                data=group,
                on_click=self.__close_anchor_group,
            ) for group in self.groups
        ]
        self.page.update()


    def __validate_group_input_field(self, e: ControlEvent) -> None:
        if self.group_input_field.value:
            self.button_group_adder.disabled = False
        else:
            self.button_group_adder.disabled = True
        self.page.update()


    def __process_reason_switch(self, e: ControlEvent) -> None:
        if self.reason_switch.value:
            self.reason_textfield.visible = False
        else:
            self.reason_textfield.value = ''
            self.reason_textfield.visible = True
        self.page.update()


    def __validate_fields(self, e: ControlEvent) -> None:
        if all([
            self.surname.value,
            self.name.value,
            self.patronymic.value,
            self.passport_serie.value,
            self.passport_number.value,
            self.address.value,
            self.institute_number.value,
            self.selected_group_id,
            self.course.value,
            self.selected_direction_id,
            self.selected_support_category_id,
        ]) and (self.reason_switch.value or self.reason_textfield.value):
            self.button_add_student.disabled = False
        else:
            self.button_add_student.disabled = True
        self.page.update()


    def __add_student(self, e: ControlEvent) -> None:
        # Validation
        if not self.passport_serie.value.isnumeric():
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Серия паспорта должна быть числом'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if len(self.passport_serie.value) != 4:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Серия паспорта должна состоять из 4 цифр'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.passport_number.value.isnumeric():
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Номер паспорта должен быть числом'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if len(self.passport_number.value) != 6:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Серия паспорта должна состоять из 6 цифр'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.institute_number.value.isnumeric() or int(self.institute_number.value) <= 0:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Номер института должен быть положительным числом'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.course.value.isnumeric() or not 1 <= int(self.course.value) <= 6:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Курс должен быть числом от 1 до 6'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.reason_switch.value:
            no_scholarship_reason = self.reason_textfield.value
        else:
            no_scholarship_reason = None
        try:
            self.db.add_student(
                self.surname.value,
                self.name.value,
                self.patronymic.value,
                self.passport_serie.value,
                self.passport_number.value,
                self.address.value,
                int(self.institute_number.value),
                self.selected_group_id,
                int(self.course.value),
                self.selected_direction_id,
                no_scholarship_reason,
                self.union_member_switch.value,
                self.selected_support_category_id,
            )
        except:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('В базе данных уже существует человек с такими же паспортными данными'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.out_function()
        self.page.snack_bar = ft.SnackBar(content=ft.Text('Студент успешно добавлен!'), show_close_icon=True)
        self.page.snack_bar.open = True
        self.page.update()
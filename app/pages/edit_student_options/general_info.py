import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from app.pages.edit_student_options import EditStudentOption


class GeneralInfo(EditStudentOption):
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function, back_function):
        super().__init__(page, db, student_id, out_function, back_function)
        self.student_info: dict = self.db.get_student_info(self.student_id)

        # Initial controls data
        self.INIT_SURNAME = str(self.student_info['surname'])
        self.INIT_NAME = str(self.student_info['name'])
        self.INIT_PATRONYMIC = str(self.student_info['patronymic'])
        self.INIT_PASSPORT_SERIE = str(self.student_info['passport_serie'])
        self.INIT_PASSPORT_NUMBER = str(self.student_info['passport_number'])
        self.INIT_ADDRESS = str(self.student_info['address'])
        self.INIT_INSTITUTE_NUMBER = str(self.student_info['institute_number'])
        self.INIT_GROUP_ID = str(self.student_info['group_id'])
        self.INIT_GROUP = str(self.student_info['group'])
        self.INIT_COURSE = str(self.student_info['course'])
        self.INIT_DIRECTION_ID = str(self.student_info['direction_id'])
        self.INIT_DIRECTION = str(self.student_info['direction'])
        self.INIT_NO_SCHOLARSHIP_REASON = str(self.student_info['no_scholarship_reason']) if self.student_info['no_scholarship_reason'] else ''
        self.INIT_IS_TRADE_UNION_MEMBER = self.student_info['is_trade_union_member']
        self.INIT_SUPPORT_CATEGORY_ID = str(self.student_info['support_category_id'])
        self.INIT_SUPPORT_CATEGORY = str(self.student_info['support_category'])

        self.groups = None
        self.selected_group_id = int(self.INIT_GROUP_ID)
        self.selected_direction_id = int(self.INIT_DIRECTION_ID)
        self.selected_support_category_id = int(self.INIT_SUPPORT_CATEGORY_ID)

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
        self.button_update_student = None


    def load_editing_page(self) -> None:
        self.groups = self.db.get_groups()

        def close_anchor_direction(e: ControlEvent) -> None:
            direction_data = e.control.data
            self.selected_direction_id = direction_data['id']
            self.direction.close_view(direction_data['name'])
            self.__validate_fields(e)
            self.page.update()

        def close_anchor_support_category(e: ControlEvent) -> None:
            self.selected_support_category_id = e.control.data['id']
            self.support_category.close_view(e.control.data['name'])
            self.__validate_fields(e)
            self.page.update()

        header = HeaderText('Редактирование общих данных студента')

        # Controls
        self.surname = TextField('Фамилия', value=self.INIT_SURNAME, on_change=self.__validate_fields)
        self.name = TextField('Имя', value=self.INIT_NAME, on_change=self.__validate_fields)
        self.patronymic = TextField('Отчество', value=self.INIT_PATRONYMIC, on_change=self.__validate_fields)
        self.passport_serie = TextField('Серия паспорта', value=self.INIT_PASSPORT_SERIE, on_change=self.__validate_fields)
        self.passport_number = TextField('Номер паспорта', value=self.INIT_PASSPORT_NUMBER, on_change=self.__validate_fields)
        self.address = TextField('Адрес', value=self.INIT_ADDRESS, on_change=self.__validate_fields, width=1000)
        self.institute_number = TextField('Номер института', value=self.INIT_INSTITUTE_NUMBER, on_change=self.__validate_fields)

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
            on_tap=self.__validate_fields,
            width=300,
        )
        self.group.value = self.INIT_GROUP

        self.group_adder = ft.IconButton(icon=ft.icons.ADD_CIRCLE, tooltip='Добавить группу', on_click=self.__enter_group)
        self.group_input_field = TextField('Новая группа', visible=False, on_change=self.__validate_group_input_field)
        self.button_group_adder = ft.OutlinedButton('Добавить', visible=False, disabled=True, on_click=self.__add_group)

        self.course = TextField('Курс', value=self.INIT_COURSE, on_change=self.__validate_fields)
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
        self.direction.value = self.INIT_DIRECTION

        gets_scholarship = False if self.INIT_NO_SCHOLARSHIP_REASON else True
        self.reason_text = Text('Имеет право получать стипендию?')
        self.reason_switch = ft.Switch(value=gets_scholarship, on_change=self.__process_reason_switch)
        self.reason_textfield = TextField(
            'Почему не имеет?',
            value=self.INIT_NO_SCHOLARSHIP_REASON,
            visible=not gets_scholarship,
            on_change=self.__validate_fields
        )

        self.union_member_text = Text('Член профсоюза?')
        self.union_member_switch = ft.Switch(value=self.INIT_IS_TRADE_UNION_MEMBER, on_change=self.__validate_fields)
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
        self.support_category.value = self.INIT_SUPPORT_CATEGORY
        self.selected_support_category_id = int(self.INIT_SUPPORT_CATEGORY_ID)

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.back_function())
        self.button_update_student = ft.ElevatedButton('Обновить данные', disabled=True, on_click=self.__update_student)

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
                ft.Row([self.button_back, self.button_update_student], alignment=ft.MainAxisAlignment.CENTER),
            ],
            expand=1,
            spacing=20,
            padding=10,
        ))


    def __close_anchor_group(self, e: ControlEvent) -> None:
        self.selected_group_id = e.control.data['id']
        print(f'{self.selected_group_id = }')
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
            self.reason_textfield.visible = True
        self.reason_textfield.value = ''
        self.__validate_fields(e)
        self.page.update()


    def __validate_fields(self, e: ControlEvent) -> None:
        init_gets_scholarship = False if self.INIT_NO_SCHOLARSHIP_REASON else True
        if all([
            self.surname.value,
            self.name.value,
            self.patronymic.value,
            self.passport_serie.value,
            self.passport_number.value,
            self.address.value,
            self.institute_number.value,
            self.group.value,
            self.course.value,
            self.direction.value,
        ]) and (self.reason_switch.value or self.reason_textfield.value):
            if any([
                self.surname.value != self.INIT_SURNAME,
                self.name.value != self.INIT_NAME,
                self.patronymic.value != self.INIT_PATRONYMIC,
                self.passport_serie.value != self.INIT_PASSPORT_SERIE,
                self.passport_number.value != self.INIT_PASSPORT_NUMBER,
                self.address.value != self.INIT_ADDRESS,
                self.institute_number.value != self.INIT_INSTITUTE_NUMBER,
                str(self.selected_group_id) != self.INIT_GROUP_ID,
                self.course.value != self.INIT_COURSE,
                str(self.selected_direction_id) != self.INIT_DIRECTION_ID,
                self.reason_switch.value != init_gets_scholarship,
                self.reason_textfield.value != self.INIT_NO_SCHOLARSHIP_REASON,
                self.union_member_switch.value != self.INIT_IS_TRADE_UNION_MEMBER,
                str(self.selected_support_category_id) != self.INIT_SUPPORT_CATEGORY_ID,
            ]):
                self.button_update_student.disabled = False
            else:
                self.button_update_student.disabled = True
        else:
            self.button_update_student.disabled = True
        self.page.update()


    def __update_student(self, e: ControlEvent):
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
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Номер паспорта должен состоять из 6 цифр'), show_close_icon=True)
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
        if not self.group.value:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Заполните поле "Группа"'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.direction.value:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Заполните поле "Направление"'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.support_category.value:
            self.page.snack_bar = ft.SnackBar(content=ft.Text('Заполните поле "Категория поддержки"'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.reason_switch.value:
            no_scholarship_reason = self.reason_textfield.value
        else:
            no_scholarship_reason = None
        try:
            self.db.update_student(
                self.student_id,
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
            self.db.cur.execute('ROLLBACK;')
            self.page.snack_bar = ft.SnackBar(content=ft.Text('В базе данных уже существует человек с такими же паспортными данными'), show_close_icon=True)
            self.page.snack_bar.open = True
            self.page.update()
            return

        self.page.snack_bar = ft.SnackBar(content=ft.Text('Данные успешно обновлены!'), show_close_icon=True)
        self.page.snack_bar.open = True
        self.page.update()
        self.back_function()
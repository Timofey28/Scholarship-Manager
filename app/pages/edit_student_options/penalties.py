import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from . import EditStudentOption


class Penalties(EditStudentOption):
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function, back_function):
        super().__init__(page, db, student_id, out_function, back_function)
        self.student_info: dict = self.db.get_student_info(self.student_id)
        self.student_fio: str = self.student_info['surname'] + ' ' + self.student_info['name'] + ' ' + self.student_info['patronymic']
        self.penalties: list[dict] = self.db.get_student_penalties(self.student_id)
        self.init_penalties: dict = {penalty['name']: penalty['amount'] for penalty in self.penalties}

        # Controls
        self.button_trade_union = None
        self.cr_union_penalty = None
        self.cr_penalties_phrase = None
        self.cr_penalties = None
        self.button_add_penalty = None
        self.button_back = None
        self.button_save = None


    def load_editing_page(self) -> None:
        header = HeaderText('Редактирование вычетов и штрафов')
        student_name = Text('Студент: ' + self.student_fio)
        self.cr_union_penalty = ft.ListTile(
            trailing=Text('1%'),
            title=Text('Профсоюзный вычет', size=18),
            leading=ft.Icon(ft.icons.PAYMENT),
            visible=self.student_info['is_trade_union_member'],
        )
        self.button_trade_union = ft.Chip(
            label=Text('Удалить профсоюзный вычет') if self.student_info['is_trade_union_member'] else ft.Text('Добавить профсоюзный вычет'),
            leading=ft.Icon(ft.icons.HOME),
            on_click=self.__trade_union,
        )
        self.cr_penalties_phrase = Text('Штрафы:')
        self.cr_penalties = ft.ListView(
            controls=[
                ft.ListTile(
                    title=Text(penalty['name']),
                    subtitle=SmallText(f"{penalty['amount']:_}".replace('_', '.') + ',00 ₽'),
                    leading=ft.Icon(ft.icons.PAYMENT),
                    trailing=ft.IconButton(icon=ft.icons.DELETE, data=penalty, tooltip='Удалить штраф', on_click=self.__delete_penalty),
                    on_click=self.__edit_penalty,
                    data=penalty,
                )
                for penalty in self.penalties
            ],
            expand=1,
            width=500,
            spacing=10,
        )
        self.cr_penalties.controls.sort(key=lambda x: x.title.value)
        self.button_add_penalty = ft.Chip(
            label=Text('Добавить штраф'),
            leading=ft.Icon(ft.icons.ADD),
            on_click=self.__add_penalty,
        )

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.back_function())
        self.button_save = ft.ElevatedButton('Сохранить', disabled=True, on_click=self.__save_penalties)

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=student_name, margin=ft.margin.only(left=200)),
            ft.Container(content=self.button_trade_union, margin=ft.margin.only(left=200)),
            ft.Container(content=self.cr_union_penalty, bgcolor=ft.colors.BLUE_900, border_radius=15, width=800, margin=ft.margin.only(left=200)),
            ft.Divider(),

            ft.Container(content=self.cr_penalties_phrase, margin=ft.margin.only(left=200)),
            ft.Container(content=self.button_add_penalty, margin=ft.margin.only(left=200)),
            ft.Container(content=self.cr_penalties, bgcolor=ft.colors.BLUE_900, border_radius=15, width=800, margin=ft.margin.only(left=200)),
            ft.Row([self.button_back, self.button_save], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )


    def __trade_union(self, e: ControlEvent) -> None:
        if self.cr_union_penalty.visible:
            self.cr_union_penalty.visible = False
            self.button_trade_union.label.value = 'Добавить профсоюзный вычет'
        else:
            self.cr_union_penalty.visible = True
            self.button_trade_union.label.value = 'Удалить профсоюзный вычет'
        self.__validate_fields(e)
        self.page.update()


    def __delete_penalty(self, e: ControlEvent) -> None:
        for penalty in self.cr_penalties.controls:
            if penalty.data == e.control.data:
                self.cr_penalties.controls.remove(penalty)
                break
        self.__validate_fields(e)
        self.page.update()


    def __edit_penalty(self, e: ControlEvent) -> None:
        def validate(ee: ControlEvent) -> None:
            if penalty_name.value and penalty_amount.value:
                if type(penalty_amount.value) is int and penalty_amount.value > 0 and penalty_amount.value != e.control.data['amount']:
                    button_save.disabled = False
                elif type(penalty_amount.value) is str and penalty_amount.value.isdigit() and int(penalty_amount.value) > 0 and int(penalty_amount.value) != e.control.data['amount']:
                    button_save.disabled = False
                elif penalty_name.value != e.control.data['name']:
                    button_save.disabled = False
                else:
                    button_save.disabled = True
            else:
                button_save.disabled = True
            self.page.update()

        def cancel(ee: ControlEvent) -> None:
            self.page.overlay.clear()
            self.page.update()

        def update_penalty(ee: ControlEvent) -> None:
            for penalty in self.cr_penalties.controls:
                if penalty.data == e.control.data:
                    penalty.title.value = penalty_name.value
                    penalty.subtitle.value = f"{int(penalty_amount.value):_}".replace('_', '.') + ',00 ₽'
                    penalty.data = {'name': penalty_name.value, 'amount': int(penalty_amount.value)}
                    penalty.trailing.data = {'name': penalty_name.value, 'amount': int(penalty_amount.value)}
                    break
            self.cr_penalties.controls.sort(key=lambda x: x.title.value)
            self.__validate_fields(e)
            self.page.overlay.clear()
            self.page.update()

        edit_penalty_phrase = Text('Редактирование штрафа')
        penalty_name = TextField('Название штрафа', value=e.control.data['name'], width=500, on_change=validate)
        penalty_amount = TextField('Сумма штрафа', value=e.control.data['amount'], width=200, on_change=validate)
        button_calcel = ft.ElevatedButton('Отмена', on_click=cancel)
        button_save = ft.ElevatedButton('Сохранить', disabled=True, on_click=update_penalty)
        content = ft.Container(
            content=ft.Column([edit_penalty_phrase, penalty_name, penalty_amount, button_calcel, button_save]),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
            width=600,
            height=300,
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


    def __add_penalty(self, e: ControlEvent) -> None:
        def validate(e: ControlEvent) -> None:
            if penalty_name.value and penalty_amount.value:
                if penalty_amount.value.isdigit() and int(penalty_amount.value) > 0:
                    button_add.disabled = False
                else:
                    button_add.disabled = True
            else:
                button_add.disabled = True
            self.page.update()

        def cancel(e: ControlEvent) -> None:
            self.page.overlay.clear()
            self.page.update()

        def add_penalty_to_list(e: ControlEvent) -> None:
            self.cr_penalties.controls.append(
                ft.ListTile(
                    title=Text(penalty_name.value),
                    subtitle=SmallText(f"{int(penalty_amount.value):_}".replace('_', '.') + ',00 ₽'),
                    leading=ft.Icon(ft.icons.PAYMENT),
                    trailing=ft.IconButton(icon=ft.icons.DELETE, data={'name': penalty_name.value, 'amount': int(penalty_amount.value)}, tooltip='Удалить штраф', on_click=self.__delete_penalty),
                    on_click=self.__edit_penalty,
                    data={'name': penalty_name.value, 'amount': int(penalty_amount.value)},
                )
            )
            self.cr_penalties.controls.sort(key=lambda x: x.title.value)
            self.__validate_fields(e)
            self.page.overlay.clear()
            self.page.update()

        new_penalty_phrase = Text('Добавление нового штрафа')
        penalty_name = TextField('Название штрафа', width=500, on_change=validate)
        penalty_amount = TextField('Сумма штрафа', width=200, on_change=validate)
        button_calcel = ft.ElevatedButton('Отмена', on_click=cancel)
        button_add = ft.ElevatedButton('Добавить', disabled=True, on_click=add_penalty_to_list)
        content = ft.Container(
            content=ft.Column([new_penalty_phrase, penalty_name, penalty_amount, button_calcel, button_add]),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
            width=600,
            height=300,
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


    def __validate_fields(self, e: ControlEvent) -> None:
        save_button_should_be_disabled = True
        if self.cr_union_penalty.visible != self.student_info['is_trade_union_member']:
            save_button_should_be_disabled = False
        else:
            initial_penalties_left = 0
            for penalty in self.cr_penalties.controls:
                penalty_name = penalty.data['name']
                penalty_amount = penalty.data['amount']
                if penalty_name not in self.init_penalties:
                    save_button_should_be_disabled = False
                    break
                if penalty_amount != self.init_penalties[penalty_name]:
                    save_button_should_be_disabled = False
                    break
                initial_penalties_left += 1
            if save_button_should_be_disabled:
                if initial_penalties_left != len(self.init_penalties):
                    save_button_should_be_disabled = False

        if save_button_should_be_disabled:
            self.button_save.disabled = True
        else:
            self.button_save.disabled = False
        self.page.update()


    def __save_penalties(self, e: ControlEvent) -> None:
        if self.cr_union_penalty.visible != self.student_info['is_trade_union_member']:
            self.db.update_student(
                self.student_id,
                self.student_info['surname'],
                self.student_info['name'],
                self.student_info['patronymic'],
                self.student_info['passport_serie'],
                self.student_info['passport_number'],
                self.student_info['address'],
                self.student_info['institute_number'],
                self.student_info['group_id'],
                self.student_info['course'],
                self.student_info['direction_id'],
                self.student_info['no_scholarship_reason'],
                self.cr_union_penalty.visible,
                self.student_info['support_category_id'],
            )

        penalties = []
        for penalty in self.cr_penalties.controls:
            penalties.append((penalty.data['name'], penalty.data['amount']))
        self.db.update_student_penalties(self.student_id, penalties)
        self.back_function()
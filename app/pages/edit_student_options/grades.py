from time import sleep
import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from . import EditStudentOption


class Grades(EditStudentOption):
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function, back_function):
        super().__init__(page, db, student_id, out_function, back_function)
        self.student_info: dict = self.db.get_student_info(self.student_id)
        self.student_fio: str = self.student_info['surname'] + ' ' + self.student_info['name'] + ' ' + self.student_info['patronymic']
        self.grades: list[dict] = self.db.get_student_grades(self.student_id)
        self.init_grades: dict = {grade['subject_id']: str(grade['grade']) for grade in self.grades}
        self.other_subjects: list[dict] = self.db.get_other_subjects(self.student_id)

        # Controls
        self.search_bar = None
        self.cr_grades_list = None
        self.button_back = None
        self.button_save = None


    def load_editing_page(self) -> None:
        header = HeaderText('Редактирование оценок')
        student_name = Text('Студент: ' + self.student_fio)
        self.search_bar = ft.SearchBar(
            view_elevation=4,
            divider_color=ft.colors.AMBER,
            bar_hint_text='Добавить предмет',
            view_hint_text='Выберите предмет из списка...',
            controls=[
                ft.ListTile(
                    title=ft.Text(subject['name']),
                    data=subject,
                    on_click=self.__add_subject,
                ) for subject in self.other_subjects
            ],
            on_change=self.__validate_fields,
            width=1000,
        )
        self.search_bar.controls.append(
            ft.ListTile(
                leading=ft.Icon(ft.icons.ADD),
                title=ft.Text('Добавить новый предмет'),
                data=0,
                on_click=self.__add_subject,
            )
        )

        self.cr_grades_list = ft.ListView(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SUBJECT),
                    title=ft.Text(grade['subject_name']),
                    trailing=ft.Row(
                        controls=[
                            TextField('Оценка', width=90, value=str(grade['grade']), on_change=self.__validate_fields),
                            ft.IconButton(
                                ft.icons.DELETE,
                                tooltip='Удалить предмет',
                                data={'id': grade['subject_id'], 'name': grade['subject_name']},
                                on_click=self.__remove_subject
                            ),
                        ],
                        width=150
                    ),
                    data={'subject_id': grade['subject_id'], 'subject_name': grade['subject_name']},
                ) for grade in self.grades
            ],
            width=500,
            spacing=10,
            expand=1
        )

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.back_function())
        self.button_save = ft.ElevatedButton('Сохранить', disabled=True, on_click=self.__save_grades)

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=student_name, margin=ft.margin.only(left=200)),
            ft.Row([self.search_bar], alignment=ft.MainAxisAlignment.CENTER),
            # ft.Container(self.cr_grades_list, margin=ft.margin.only(left=200)),  # нельзя листать список
            self.cr_grades_list,  # нельзя отступить от левого края
            ft.Row([self.button_back, self.button_save], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )


    def __add_subject(self, e: ControlEvent) -> None:
        def validate(e: ControlEvent) -> None:
            if subject.value != '':
                button_add.disabled = False
            else:
                button_add.disabled = True
            self.page.update()

        def cancel(e: ControlEvent) -> None:
            self.page.overlay.clear()
            self.page.update()

        def add_subject_to_list(e: ControlEvent) -> None:
            new_subject_id = self.db.create_subject(subject.value)
            self.cr_grades_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SUBJECT),
                    title=ft.Text(subject.value),
                    trailing=ft.Row(
                        controls=[
                            TextField('Оценка', width=90, on_change=self.__validate_fields),
                            ft.IconButton(ft.icons.DELETE, tooltip='Удалить предмет', data={'id': new_subject_id, 'name': subject.value}, on_click=self.__remove_subject),
                        ],
                        width=150,
                    ),
                    data={'subject_id': new_subject_id, 'subject_name': subject.value},
                )
            )
            self.cr_grades_list.controls.sort(key=lambda x: x.title.value)
            self.page.overlay.clear()
            self.__validate_fields(e)
            self.page.update()

        self.search_bar.close_view()
        sleep(0.1)
        if e.control.data:
            subject_id, subject_name = e.control.data['id'], e.control.data['name']
            self.search_bar.controls = [control for control in self.search_bar.controls if control.data != e.control.data]
            self.cr_grades_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SUBJECT),
                    title=ft.Text(subject_name),
                    trailing=ft.Row(
                        controls=[
                            TextField('Оценка', width=90, on_change=self.__validate_fields),
                            ft.IconButton(ft.icons.DELETE, tooltip='Удалить предмет', data={'id': subject_id, 'name': subject_name}, on_click=self.__remove_subject),
                        ],
                        width=150,
                    ),
                    data={'subject_id': subject_id, 'subject_name': subject_name},
                )
            )
            self.cr_grades_list.controls.sort(key=lambda x: x.title.value)
            self.__validate_fields(e)
            self.page.update()
        else:
            subject = TextField('Новый предмет', width=500, on_change=validate)
            button_calcel = ft.ElevatedButton('Отмена', on_click=cancel)
            button_add = ft.ElevatedButton('Добавить', disabled=True, on_click=add_subject_to_list)
            content = ft.Container(
                content=ft.Column([subject, button_calcel, button_add]),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20),
                width=600,
                height=200,
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


    def __remove_subject(self, e: ControlEvent) -> None:
        self.cr_grades_list.controls = [control for control in self.cr_grades_list.controls if control.data['subject_id'] != e.control.data['id']]
        adder = self.search_bar.controls.pop()
        self.search_bar.controls.append(
            ft.ListTile(
                title=ft.Text(e.control.data['name']),
                data={'id': e.control.data['id'], 'name': e.control.data['name']},
                on_click=self.__add_subject,
            )
        )
        self.search_bar.controls.sort(key=lambda x: x.title.value)
        self.search_bar.controls.append(adder)
        self.__validate_fields(e)
        self.page.update()


    def __validate_fields(self, e: ControlEvent) -> None:
        save_button_should_be_disabled = False
        initial_grades_left = 0
        new_subjects_amount = 0
        for grade_tile in self.cr_grades_list.controls:
            subject_id = grade_tile.data['subject_id']
            grade_value = grade_tile.trailing.controls[0].value
            if grade_value == '':
                save_button_should_be_disabled = True
                break
            if subject_id in self.init_grades:
                initial_grades_left += 1
            else:
                new_subjects_amount += 1

        if save_button_should_be_disabled:
            self.button_save.disabled = True
        else:
            if initial_grades_left == len(self.init_grades) and new_subjects_amount == 0:
                changed_amount = 0
                for grade_tile in self.cr_grades_list.controls:
                    subject_id = grade_tile.data['subject_id']
                    grade_value = grade_tile.trailing.controls[0].value
                    if grade_value != self.init_grades[subject_id]:
                        changed_amount += 1
                if changed_amount == 0:
                    self.button_save.disabled = True
                else:
                    self.button_save.disabled = False
            else:
                self.button_save.disabled = False
        self.page.update()


    def __save_grades(self, e: ControlEvent) -> None:
        new_grades = []
        for grade_tile in self.cr_grades_list.controls:
            subject_id = grade_tile.data['subject_id']
            grade_value = grade_tile.trailing.controls[0].value
            try:
                grade_value = int(grade_value)
                if not 2 <= grade_value <= 5:
                    raise ValueError
            except ValueError:
                self.page.snack_bar = ft.SnackBar(content=ft.Text('Оценка должна быть любым натуральным числом от 2 до 5 включительно'), show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
                return
            new_grades.append([subject_id, grade_value])
        self.db.update_student_grades(self.student_id, new_grades)
        self.back_function()
        self.page.snack_bar = ft.SnackBar(content=ft.Text('Данные успешно сохранены!'), show_close_icon=True)
        self.page.snack_bar.open = True
        self.page.update()
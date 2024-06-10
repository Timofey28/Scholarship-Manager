from datetime import date
from typing import Optional
import flet as ft
from flet import ControlEvent
import logging

from database import Database
from data import SCHOLARSHIP_AMOUNT_4, SCHOLARSHIP_AMOUNT_5
from app.custom_controls import *


class ScholarshipCalculator:
    def __init__(self, page: ft.Page, db: Database, out_function):
        self.page = page
        self.db = db
        self.out_function = out_function
        self.page.title = 'Расчет стипендии'
        self.very_small_number = 1e-9
        self.students = self.db.get_students()
        self.orders = self.db.get_orders()
        self.scholarships_info: dict[int, dict[str, Optional[int | str | bool | date | list | dict]]] = {student['fio']: {
            'no_scholarship_reason': None,
            'initial_scholarship': None,
            'is_trade_union_member': None,
            'penalties': [],
            'orders': [],
            'support': None,
            'final_scholarship': None,
        } for student in self.students}

        '''
        {
            'student_fio': {
                'no_scholarship_reason': ... (str | None),
                'initial_scholarship': ... (int),
                'is_trade_union_member': ... (bool),
                'penalties': [
                    {
                        'amount': ... (int),
                        'name': ... (str),
                    }
                ],
                'orders': [
                    {
                        'amount': ... (int),
                        'number': ... (str),
                        'date': ... (date),
                    }
                ],
                'support': None | {
                    'amount': ... (int),
                    'category': ... (str),
                },
                'final_scholarship': ... (int),
            },
            'student_fio': {...},
            ...
        }
        '''


    def load_page(self) -> None:
        header = HeaderText('Список месячных стипендий студентов')
        button_back = ft.IconButton(icon=ft.icons.ARROW_LEFT, tooltip='Назад', on_click=lambda _: self.out_function())
        self.__get_scholarship_info()
        student_scholarships = ft.ListView(expand=1, spacing=10, width=1200)
        counter = 1
        for student_fio, scholarship_info in self.scholarships_info.items():
            if scholarship_info['no_scholarship_reason']:
                subtitle = 'Студент не получает стипендию'
                subtitle += f"\nПричина: {scholarship_info['no_scholarship_reason']}"
                trailing = None
            else:
                subtitle = f"Изначальная стипендия исходя из успеваемости студента: {self.__prettify_money(scholarship_info['initial_scholarship'])}"
                if scholarship_info['is_trade_union_member']:
                    subtitle += f"\nПрофсоюзный вычет: {self.__prettify_money(int(scholarship_info['initial_scholarship'] * 0.01))}"
                for penalty in scholarship_info['penalties']:
                    subtitle += f"\nШтраф: {self.__prettify_money(int(penalty['amount']))} ({penalty['name']})"
                for order in scholarship_info['orders']:
                    subtitle += f"\nНадбавка: {self.__prettify_money(int(order['amount']))} (приказ №{order['number']} от {order['date']:%d.%m.%Y})"
                if scholarship_info['support']['amount']:
                    subtitle += f"\nМатериальная помощь: {self.__prettify_money(int(scholarship_info['support']['amount']))} ({scholarship_info['support']['category']})"
                subtitle += f"\nИтоговая стипендия: {self.__prettify_money(scholarship_info['final_scholarship'])}"
                trailing = ft.Text(self.__prettify_money(scholarship_info['final_scholarship']), size=25)
            student_scholarships.controls.append(
                ft.ListTile(
                    leading=Text(f'{counter})'),
                    title=Text(f'{student_fio}'),
                    subtitle=SmallText(subtitle),
                    trailing=trailing,
                    bgcolor=ft.colors.BLUE_GREY_900,
                )
            )
            counter += 1

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            button_back,
            student_scholarships,
        )


    def __get_scholarship_info(self) -> None:
        for student in self.students:
            student_id = student['id']
            student_fio = student['fio']
            final_scholarship = 0.0

            # 0) Right to receive scholarship
            if student['no_scholarship_reason']:
                self.scholarships_info[student_fio]['no_scholarship_reason'] = student['no_scholarship_reason']
                continue

            # 1) Initial scholarship
            minimum_grade = self.__get_student_minimum_grade(student_id)
            if minimum_grade == 4:
                self.scholarships_info[student_fio]['initial_scholarship'] = SCHOLARSHIP_AMOUNT_4
                final_scholarship += SCHOLARSHIP_AMOUNT_4
            elif minimum_grade == 5:
                self.scholarships_info[student_fio]['initial_scholarship'] = SCHOLARSHIP_AMOUNT_5
                final_scholarship += SCHOLARSHIP_AMOUNT_5
            else:
                if minimum_grade == 0:
                    logging.warning(f'Student ({student_id}) has no grades')
                self.scholarships_info[student_fio]['initial_scholarship'] = 0

            # 2) Trade union membership
            self.scholarships_info[student_fio]['is_trade_union_member'] = student['is_trade_union_member']
            if student['is_trade_union_member']:
                final_scholarship *= 0.99

            # 3) Penalties
            self.scholarships_info[student_fio]['penalties'] = self.db.get_student_penalties(student_id)
            for penalty in self.scholarships_info[student_fio]['penalties']:
                final_scholarship -= penalty['amount'] / 6

            # 4) Orders
            for order in self.orders:
                if order['student_id'] is not None and order['student_id'] == student_id or \
                        order['group_id'] is not None and order['group_id'] == student['group_id'] or \
                        order['institute_number'] is not None and order['institute_number'] == student['institute_number']:
                    self.scholarships_info[student_fio]['orders'].append({
                        'amount': order['enrollment_amount'],
                        'number': order['number'],
                        'date': order['date'],
                    })
                    final_scholarship += order['enrollment_amount'] / 6

            # 5) Support
            if student['sc_semester_payment']:
                self.scholarships_info[student_fio]['support'] = {
                    'amount': student['sc_semester_payment'],
                    'category': student['sc_name'],
                }
                final_scholarship += student['sc_semester_payment'] / 6
            else:
                self.scholarships_info[student_fio]['support'] = None

            # 6) Final scholarship
            self.scholarships_info[student_fio]['final_scholarship'] = round(final_scholarship)


    def __get_student_minimum_grade(self, student_id: int) -> int:
        grades = self.db.get_student_grades(student_id)
        if not grades:
            return 0
        return min([grade['grade'] for grade in grades])


    def __prettify_money(self, money: int) -> str:
        money = float(round(money, 2))
        return f'{money:_}'.replace('.', ',').replace('_', '.') + f"{'0 ₽' if money * 10 % 1 < self.very_small_number else ' ₽'}"
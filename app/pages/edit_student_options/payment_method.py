import flet as ft
from flet import ControlEvent

from database import Database
from app.custom_controls import *
from . import EditStudentOption


class PaymentMethod(EditStudentOption):
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function, back_function):
        super().__init__(page, db, student_id, out_function, back_function)
        self.student_info: dict = self.db.get_student_info(self.student_id)
        self.student_fio = self.student_info['surname'] + ' ' + self.student_info['name'] + ' ' + self.student_info['patronymic']
        self.payment_method_info: dict = self.db.get_payment_method_info(self.student_id)

        self.IN_CASH = 'in_cash'
        self.BANK_CARD = 'bank_card'
        self.PAYMENT_ACCOUNT = 'payment_account'

        # Controls
        self.cr_dropdown_choose_type = None
        self.cr_bank = None
        self.cr_phone_number = None
        self.cr_payment_account = None
        self.button_back = None
        self.button_save = None


    def load_editing_page(self) -> None:
        header = HeaderText('Редактирование способа выплаты стипендии')
        student_name = Text('Студент: ' + self.student_fio)

        self.cr_dropdown_choose_type = ft.Dropdown(
            width=300,
            options=[
                ft.dropdown.Option(text='Наличными', key=self.IN_CASH),
                ft.dropdown.Option(text='На банковскую карту', key=self.BANK_CARD),
                ft.dropdown.Option(text='На расчетный счет', key=self.PAYMENT_ACCOUNT),
            ],
            on_change=self.__validate_fields,
        )
        self.cr_dropdown_choose_type.value = self.payment_method_info['type']
        self.cr_bank = TextField('Банк', width=200, value=self.payment_method_info['bank'], visible=False, on_change=self.__validate_fields)
        self.cr_phone_number = TextField('Номер телефона', width=200, value=self.payment_method_info['phone_number'], visible=False, on_change=self.__validate_fields)
        self.cr_payment_account = TextField('Расчетный счет', width=300, value=self.payment_method_info['payment_account'], visible=False, on_change=self.__validate_fields)
        if self.cr_dropdown_choose_type.value == self.BANK_CARD:
            self.cr_bank.visible = True
            self.cr_phone_number.visible = True
        elif self.cr_dropdown_choose_type.value == self.PAYMENT_ACCOUNT:
            self.cr_payment_account.visible = True

        self.button_back = ft.ElevatedButton('Назад', on_click=lambda _: self.back_function())
        self.button_save = ft.ElevatedButton('Сохранить', disabled=True, on_click=self.__save_payment_method)

        self.page.clean()
        self.page.add(
            ft.Row([header], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=student_name, margin=ft.margin.only(left=200)),
            ft.Container(
                content=ft.Row(
                    [
                        Text('Тип выплаты:'),
                        self.cr_dropdown_choose_type,
                        ft.Container(content=ft.Column([self.cr_bank, self.cr_phone_number, self.cr_payment_account]))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                margin=ft.margin.only(top=15, bottom=15),
            ),
            ft.Row([self.button_back, self.button_save], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        )


    def __validate_fields(self, e: ControlEvent) -> None:
        if self.cr_dropdown_choose_type.value == self.BANK_CARD:
            self.cr_bank.visible = True
            self.cr_phone_number.visible = True
            self.cr_payment_account.visible = False
        elif self.cr_dropdown_choose_type.value == self.PAYMENT_ACCOUNT:
            self.cr_bank.visible = False
            self.cr_phone_number.visible = False
            self.cr_payment_account.visible = True
        else:
            self.cr_bank.visible = False
            self.cr_phone_number.visible = False
            self.cr_payment_account.visible = False

        if self.cr_dropdown_choose_type.value != self.payment_method_info['type']:
            if any([
                self.cr_dropdown_choose_type.value == self.IN_CASH,
                self.cr_dropdown_choose_type.value == self.BANK_CARD and self.cr_bank.value != '' and self.cr_phone_number.value != '',
                self.cr_dropdown_choose_type.value == self.PAYMENT_ACCOUNT and self.cr_payment_account.value != '',
            ]):
                self.button_save.disabled = False
            else:
                self.button_save.disabled = True
        else:
            if any([
                self.cr_dropdown_choose_type.value == self.BANK_CARD and self.cr_bank.value != '' and self.cr_bank.value != self.payment_method_info['bank'] or
                    self.cr_phone_number.value != '' and self.cr_phone_number.value != self.payment_method_info['phone_number'],
                self.cr_dropdown_choose_type.value == self.PAYMENT_ACCOUNT and self.cr_payment_account.value != '' and
                    self.cr_payment_account.value != self.payment_method_info['payment_account'],
            ]):
                self.button_save.disabled = False
            else:
                self.button_save.disabled = True
        self.page.update()


    def __save_payment_method(self, e: ControlEvent) -> None:
        # Validate data
        if self.cr_dropdown_choose_type.value == self.BANK_CARD:
            phone_number = self.cr_phone_number.value
            for char in phone_number:
                if char in ['(', ')', '-', ' ']:
                    phone_number = phone_number.replace(char, '')
            if not phone_number.isnumeric():
                self.page.snack_bar = ft.SnackBar(content=ft.Text('Номер телефона должен состоять из цифр'), show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
                return
            if len(phone_number) != 10 and len(phone_number) != 11:
                self.page.snack_bar = ft.SnackBar(content=ft.Text('Некорректный номер телефона'), show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.cr_phone_number.value = phone_number

        elif self.cr_dropdown_choose_type.value == self.PAYMENT_ACCOUNT:
            if not self.cr_payment_account.value.isnumeric() or len(self.cr_payment_account.value) != 20:
                self.page.snack_bar = ft.SnackBar(content=ft.Text('Расчетный счет должен состоять из 20 цифр'), show_close_icon=True)
                self.page.snack_bar.open = True
                self.page.update()
                return

        self.db.update_payment_method_info(
            student_id=self.student_id,
            type_=self.cr_dropdown_choose_type.value,
            bank=self.cr_bank.value,
            phone_number=self.cr_phone_number.value,
            payment_account=self.cr_payment_account.value,
        )
        self.page.snack_bar = ft.SnackBar(content=ft.Text('Данные успешно сохранены!'), show_close_icon=True)
        self.page.snack_bar.open = True
        self.page.update()
        self.back_function()
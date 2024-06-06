import flet as ft

from database import Database
from app.custom_controls import *


class EditStudent:
    def __init__(self, page: ft.Page, db: Database, student_id: int):
        self.page = page
        self.page.title = 'Редактирование данных студента'

    def load_page(self):
        pass
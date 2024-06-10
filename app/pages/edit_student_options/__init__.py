from abc import ABC, abstractmethod
import flet as ft
from flet import ControlEvent

from database import Database


class EditStudentOption(ABC):
    def __init__(self, page: ft.Page, db: Database, student_id: int, out_function, back_function):
        self.page = page
        self.db = db
        self.student_id = student_id
        self.out_function = out_function
        self.back_function = back_function

    @abstractmethod
    def load_editing_page(self) -> None:
        pass
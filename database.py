from datetime import date
import psycopg2


class Database:
    def __init__(self, db_dbname: str, db_host: str, db_user: str, db_password: str):
        self.conn = psycopg2.connect(dbname=db_dbname,
                                     host=db_host,
                                     user=db_user,
                                     password=db_password)
        self.cur = self.conn.cursor()

        files = [
            'sql/employee.sql',
            'sql/student.sql',
            'sql/group.sql',
            'sql/direction.sql',
            'sql/support_category.sql',
        ]

        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                self.cur.execute(f.read())


    ### Авторизация ###
    def login_employee(self, login: str, password: str) -> int:
        self.cur.execute(f"SELECT login_employee('{login}', '{password}');")
        res = self.cur.fetchall()[0][0]
        if res is None:
            return 0
        return res


    ### Студенты ###
    def get_students(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_students();")
        res = self.cur.fetchall()
        students = []
        for student in res:
            students.append({
                'id': student[0],
                'fio': student[1],
                'group': student[2],
            })
        return students

    def add_student(
            self,
            surname: str,
            name: str,
            patronymic: str,
            passport_serie: str,
            passport_number: str,
            address: str,
            institute_number: int,
            group_id: int,
            course: int,
            direction_id: int,
            no_scholarship_reason: str | None,
            is_trade_union_member: bool,
            support_category_id: int,
    ) -> int:
        if not no_scholarship_reason:
            no_scholarship_reason = 'NULL'
        else:
            no_scholarship_reason = f"'{no_scholarship_reason}'"
        self.cur.execute(f"SELECT * FROM add_student("
                         f"'{surname}', "
                         f"'{name}', "
                         f"'{patronymic}', "
                         f"'{passport_serie}', "
                         f"'{passport_number}', "
                         f"'{address}', "
                         f"{institute_number}, "
                         f"{group_id}, "
                         f"{course}, "
                         f"{direction_id}, "
                         f"{no_scholarship_reason}, "
                         f"{is_trade_union_member}, "
                         f"{support_category_id});")
        self.conn.commit()
        return self.cur.fetchall()[0][0]


    ### Группы ###
    def get_groups(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_groups();")
        res = self.cur.fetchall()
        groups = []
        for group in res:
            groups.append({
                'id': group[0],
                'name': group[1],
            })
        return groups

    def add_group(self, name: str) -> None:
        self.cur.execute(f"SELECT add_group('{name}');")
        self.conn.commit()


    ### Направления ###
    def get_directions(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_directions();")
        res = self.cur.fetchall()
        directions = []
        for direction in res:
            directions.append({
                'id': direction[0],
                'code': direction[1],
                'name': direction[2],
            })
        return directions


    ### Категории поддержки ###
    def get_support_categories(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_support_categories();")
        res = self.cur.fetchall()
        categories = []
        for category in res:
            categories.append({
                'id': category[0],
                'name': category[1],
                'semester_payment': category[2],
            })
        return categories
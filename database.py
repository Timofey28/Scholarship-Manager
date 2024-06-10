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
            'sql/init.sql',
            'sql/employee.sql',
            'sql/student.sql',
            'sql/group.sql',
            'sql/direction.sql',
            'sql/support_category.sql',
            'sql/payment_method.sql',
            'sql/grades.sql',
            'sql/penalty.sql',
            'sql/order.sql',
        ]

        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                self.cur.execute(f.read())


    ### Авторизация/сотрудники ###
    def login_employee(self, login: str, password: str) -> int:
        self.cur.execute(f"SELECT login_employee('{login}', '{password}');")
        res = self.cur.fetchall()[0][0]
        if res is None:
            return 0
        return res

    def get_employees(self) -> list[str]:
        self.cur.execute(f"SELECT * FROM get_employees();")
        res = self.cur.fetchall()
        employees = []
        for employee in res:
            employees.append(employee[0])
        return employees

    def create_employee(self, login: str, password: str) -> int:
        self.cur.execute(f"SELECT * FROM create_employee('{login}', '{password}');")
        self.conn.commit()
        return self.cur.fetchall()[0][0]

    def delete_employee(self, login: str) -> None:
        self.cur.execute(f"SELECT delete_employee('{login}');")
        self.conn.commit()


    ### Студенты ###
    def get_students(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_students();")
        res = self.cur.fetchall()
        students = []
        for student in res:
            students.append({
                'id': student[0],
                'fio': student[1],
                'institute_number': student[2],
                'group_id': student[3],
                'group': student[4],
                'no_scholarship_reason': student[5],
                'is_trade_union_member': student[6],
                'sc_name': student[7],
                'sc_semester_payment': student[8],
            })
        return students

    def get_student_info(self, student_id: int) -> dict:
        self.cur.execute(f"SELECT * FROM get_student_info({student_id}::INT);")
        res = self.cur.fetchall()[0]
        student = {
            'surname': res[0],
            'name': res[1],
            'patronymic': res[2],
            'passport_serie': res[3],
            'passport_number': res[4],
            'address': res[5],
            'institute_number': res[6],
            'group_id': res[7],
            'group': res[8],
            'course': res[9],
            'direction_id': res[10],
            'direction': res[11],
            'no_scholarship_reason': res[12],
            'is_trade_union_member': res[13],
            'support_category_id': res[14],
            'support_category': res[15]
        }
        return student

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

    def update_student(
            self,
            student_id: int,
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
    ) -> None:
        if not no_scholarship_reason:
            no_scholarship_reason = 'NULL'
        else:
            no_scholarship_reason = f"'{no_scholarship_reason}'"
        self.cur.execute(f"SELECT update_student("
                         f"{student_id}, "
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

    def get_unique_institute_numbers(self) -> list[int]:
        self.cur.execute(f"SELECT * FROM get_unique_institute_numbers();")
        res = self.cur.fetchall()
        institute_numbers = []
        for number in res:
            institute_numbers.append(number[0])
        return institute_numbers


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


    ### Способы выплаты стипендии ###
    def get_payment_method_info(self, student_id: int) -> dict:
        self.cur.execute(f"SELECT * FROM get_payment_method_info({student_id}::INT);")
        res = self.cur.fetchall()
        if res:
            res = res[0]
            return {
                'type': res[0],
                'bank': res[1],
                'phone_number': res[2],
                'payment_account': res[3],
            }
        return {
            'type': '',
            'bank': '',
            'phone_number': '',
            'payment_account': '',
        }

    def update_payment_method_info(
            self,
            student_id: int,
            type_: str,
            bank: str,
            phone_number: str,
            payment_account: str,
    ) -> None:
        self.cur.execute(f"SELECT update_payment_method_info("
                         f"{student_id}, "
                         f"'{type_}', "
                         f"'{bank}', "
                         f"'{phone_number}', "
                         f"'{payment_account}');")
        self.conn.commit()


    ### Оценки ###
    def get_student_grades(self, student_id: int) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_student_grades({student_id}::INT);")
        res = self.cur.fetchall()
        grades = []
        for grade in res:
            grades.append({
                'subject_id': grade[0],
                'subject_name': grade[1],
                'grade': grade[2],
            })
        return grades

    def update_student_grades(self, student_id: int, grades: list[list[int]]) -> None:
        if not grades:
            grades = [[0, 0]]
        self.cur.execute(f"SELECT update_student_grades({student_id}::INT, ARRAY{grades}::INT[][]);")
        self.conn.commit()

    def get_other_subjects(self, student_id: int) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_other_subjects({student_id}::INT);")
        res = self.cur.fetchall()
        subjects = []
        for subject in res:
            subjects.append({
                'id': subject[0],
                'name': subject[1],
            })
        return subjects

    def create_subject(self, subject_name: str) -> int:
        self.cur.execute(f"SELECT create_subject('{subject_name}');")
        self.conn.commit()
        return self.cur.fetchall()[0][0]


    ### Штрафы ###
    def get_student_penalties(self, student_id: int) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_student_penalties({student_id}::INT);")
        res = self.cur.fetchall()
        penalties = []
        for penalty in res:
            penalties.append({
                'name': penalty[0],
                'amount': penalty[1],
            })
        return penalties

    def update_student_penalties(self, student_id: int, penalties: list[tuple]) -> None:
        if not penalties:
            penalties = [('', 0)]
        self.cur.execute(f"SELECT update_student_penalties({student_id}::INT, ARRAY{penalties}::penalty[]);")
        self.conn.commit()


    ### Приказы ###
    def get_orders(self) -> list[dict]:
        self.cur.execute(f"SELECT * FROM get_orders();")
        res = self.cur.fetchall()
        orders = []
        for order in res:
            orders.append({
                'id': order[0],
                'number': order[1],
                'date': order[2],
                'scope': order[3],
                'institute_number': order[4],
                'group_id': order[5],
                'student_id': order[6],
                'enrollment_amount': order[7],
            })
        return orders

    def delete_order(self, order_id: int) -> None:
        self.cur.execute(f"SELECT delete_order({order_id}::INT);")
        self.conn.commit()

    def create_order(
            self,
            number: int,
            scope: str,
            institute_number: int | None,
            group_id: int | None,
            student_id: int | None,
            enrollment_amount: int
    ) -> int:
        if not institute_number:
            institute_number = 'NULL'
        if not group_id:
            group_id = 'NULL'
        if not student_id:
            student_id = 'NULL'
        self.cur.execute(f"SELECT * FROM create_order("
                         f"{number}, "
                         f"'{scope}', "
                         f"{institute_number}, "
                         f"{group_id}, "
                         f"{student_id}, "
                         f"{enrollment_amount});")
        self.conn.commit()
        return self.cur.fetchall()[0][0]
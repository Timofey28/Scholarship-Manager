CREATE OR REPLACE FUNCTION get_students()
RETURNS TABLE (
    id INT,
    fio TEXT,
    institute_number INT,
    group_id INT,
    group_ VARCHAR(15),
    no_scholarship_reason TEXT,
    is_trade_union_member BOOLEAN,
    sc_name TEXT,
    sc_semester_payment INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.surname || ' ' || s.name || ' ' || s.patronymic AS fio,
        s.institute_number,
        s.group_id,
        g.name,
        s.no_scholarship_reason,
        s.is_trade_union_member,
        sc.name,
        sc.semester_payment
    FROM
        students s
    JOIN
        groups g
    ON
        s.group_id = g.id
    JOIN
        support_categories sc
    ON
        s.support_category_id = sc.id
    ORDER BY
        fio;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_student_info(p_student_id INT)
RETURNS TABLE (
    surname TEXT,
    name TEXT,
    patronymic TEXT,
    passport_serie VARCHAR(4),
    passport_number VARCHAR(6),
    address TEXT,
    institute_number INT,
    group_id INT,
    group_ VARCHAR(15),
    course INT,
    direction_id INT,
    direction TEXT,
    no_scholarship_reason TEXT,
    is_trade_union_member BOOLEAN,
    support_category_id INT,
    support_category TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.surname,
        s.name,
        s.patronymic,
        s.passport_serie,
        s.passport_number,
        s.address,
        s.institute_number,
        g.id,
        g.name,
        s.course,
        d.id,
        d.name,
        s.no_scholarship_reason,
        s.is_trade_union_member,
        sc.id,
        sc.name
    FROM
        students s
    JOIN
        groups g ON s.group_id = g.id
    JOIN
        directions d ON s.direction_id = d.id
    JOIN
        support_categories sc ON s.support_category_id = sc.id
    WHERE
        s.id = p_student_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_student(
    p_surname TEXT,
    p_name TEXT,
    p_patronymic TEXT,
    p_passport_serie varchar(4),
    p_passport_number varchar(6),
    p_address TEXT,
    p_institute_number int,
    p_group_id int,
    p_course int,
    p_direction_id int,
    p_no_scholarship_reason TEXT,
    p_is_trade_union_member boolean,
    p_support_category_id int
)
RETURNS INT AS $$
DECLARE
    v_student_id INT;
BEGIN
    INSERT INTO students(
        surname,
        name,
        patronymic,
        passport_serie,
        passport_number,
        address,
        institute_number,
        group_id,
        course,
        direction_id,
        no_scholarship_reason,
        is_trade_union_member,
        support_category_id
    )
    VALUES (
        p_surname,
        p_name,
        p_patronymic,
        p_passport_serie,
        p_passport_number,
        p_address,
        p_institute_number,
        p_group_id,
        p_course,
        p_direction_id,
        p_no_scholarship_reason,
        p_is_trade_union_member,
        p_support_category_id
    )
    RETURNING id INTO v_student_id;

    RETURN v_student_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_student(
    p_student_id INT,
    p_surname TEXT,
    p_name TEXT,
    p_patronymic TEXT,
    p_passport_serie varchar(4),
    p_passport_number varchar(6),
    p_address TEXT,
    p_institute_number int,
    p_group_id int,
    p_course int,
    p_direction_id int,
    p_no_scholarship_reason TEXT,
    p_is_trade_union_member boolean,
    p_support_category_id int
)
RETURNS VOID AS $$
BEGIN
    UPDATE students
    SET
        surname = p_surname,
        name = p_name,
        patronymic = p_patronymic,
        passport_serie = p_passport_serie,
        passport_number = p_passport_number,
        address = p_address,
        institute_number = p_institute_number,
        group_id = p_group_id,
        course = p_course,
        direction_id = p_direction_id,
        no_scholarship_reason = p_no_scholarship_reason,
        is_trade_union_member = p_is_trade_union_member,
        support_category_id = p_support_category_id
    WHERE
        id = p_student_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_unique_institute_numbers()
RETURNS TABLE (
    institute_number INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        DISTINCT s.institute_number
    FROM
        students s
    ORDER BY
        institute_number;
END;
$$ LANGUAGE plpgsql;
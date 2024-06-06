CREATE OR REPLACE FUNCTION get_students()
RETURNS TABLE (
    id INT,
    fio TEXT,
    group_ VARCHAR(15)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.surname || ' ' || s.name || ' ' || s.patronymic AS fio,
        g.name
    FROM
        students s
    JOIN
        groups g
    ON
        s.group_id = g.id
    ORDER BY
        fio;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_student(
    p_surname TEXT,
    p_name TEXT,
    p_patronymic TEXT,
    p_passport_serie VARCHAR(4),
    p_passport_number VARCHAR(6),
    p_address TEXT,
    p_institute_number INT,
    p_group_id INT,
    p_course INT,
    p_direction_id INT,
    p_no_scholarship_reason TEXT,
    p_is_trade_union_member BOOLEAN,
    p_support_category_id INT
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
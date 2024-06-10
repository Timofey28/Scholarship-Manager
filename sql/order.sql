CREATE OR REPLACE FUNCTION get_orders()
RETURNS TABLE (
    id INT,
    number INT,
    date DATE,
    scope VARCHAR(9),
    institute_number INT,
    group_id INT,
    student_id INT,
    enrollment_amount INT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        o.id,
        o.number,
        o.date,
        o.scope,
        o.institute_number,
        o.group_id,
        o.student_id,
        o.enrollment_amount
    FROM
        orders o
    ORDER BY
        o.number;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_order(order_id INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM
        orders
    WHERE
        id = order_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_order(
    p_number INT,
    p_scope VARCHAR(9),
    p_institute_number INT,
    p_group_id INT,
    p_student_id INT,
    p_enrollment_amount INT
)
RETURNS INT AS $$
DECLARE
    v_order_id INT;
BEGIN
    INSERT INTO orders (
        number,
        scope,
        institute_number,
        group_id,
        student_id,
        enrollment_amount
    )
    VALUES (
        p_number,
        p_scope,
        p_institute_number,
        p_group_id,
        p_student_id,
        p_enrollment_amount
    )
    RETURNING
        id
    INTO
        v_order_id;

    RETURN v_order_id;
END;
$$ LANGUAGE plpgsql;
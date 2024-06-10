CREATE OR REPLACE FUNCTION login_employee(p_login TEXT, p_password TEXT)
RETURNS INT AS $$
DECLARE
    v_employee_id INT;
BEGIN
    SELECT
        id
    FROM
        employees
    WHERE
        login = p_login AND
        password = crypt(p_password, password)
    INTO v_employee_id;

    RETURN v_employee_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_employees()
RETURNS TABLE (login TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.login
    FROM
        employees e
    WHERE
        e.login != 'root'
    ORDER BY
        e.login;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_employee(p_login TEXT, p_password TEXT)
RETURNS INT AS $$
DECLARE
    v_employee_id INT;
BEGIN
    INSERT INTO employees (
        login,
        password
    )
    VALUES (
        p_login,
        crypt(p_password, gen_salt('md5'))
    )
    RETURNING id INTO v_employee_id;

    RETURN v_employee_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_employee(p_login TEXT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM employees
    WHERE login = p_login;
END;
$$ LANGUAGE plpgsql;
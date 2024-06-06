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
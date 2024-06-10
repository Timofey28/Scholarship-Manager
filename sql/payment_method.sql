CREATE OR REPLACE FUNCTION get_payment_method_info(p_student_id INT)
RETURNS TABLE(
    type VARCHAR(15),
    bank TEXT,
    phone_number VARCHAR(11),
    payment_account VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        pm.type,
        pm.bank,
        pm.phone_number,
        pm.payment_account
    FROM
        payment_methods pm
    WHERE
        pm.student_id = p_student_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_payment_method_info(
    p_student_id INT,
    p_type VARCHAR(15),
    p_bank TEXT,
    p_phone_number VARCHAR(11),
    p_payment_account VARCHAR(20)
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO payment_methods (student_id, type, bank, phone_number, payment_account)
    VALUES (p_student_id, p_type, p_bank, p_phone_number, p_payment_account)
    ON CONFLICT (student_id)
    DO UPDATE
    SET
        type = p_type,
        bank = p_bank,
        phone_number = p_phone_number,
        payment_account = p_payment_account;
END;
$$ LANGUAGE plpgsql;
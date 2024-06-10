CREATE OR REPLACE FUNCTION get_student_penalties(p_student_id INT)
RETURNS TABLE (
    name TEXT,
    amount INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.name,
        p.amount
    FROM
        penalties p
    WHERE
        p.student_id = p_student_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_student_penalties(p_student_id INT, p_penalties penalty[])
RETURNS VOID AS $$
DECLARE
    i INT;
BEGIN
    DELETE FROM penalties
    WHERE student_id = p_student_id;

    IF p_penalties[1].name = ''::TEXT AND p_penalties[1].amount = 0 THEN
        RETURN;
    END IF;

    FOR i IN 1..array_length(p_penalties, 1) LOOP
        INSERT INTO penalties (student_id, name, amount)
        VALUES (p_student_id, p_penalties[i].name, p_penalties[i].amount);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
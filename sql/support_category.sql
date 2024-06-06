CREATE OR REPLACE FUNCTION get_support_categories()
RETURNS TABLE (
    id INT,
    name TEXT,
    semester_payment INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        sc.id,
        sc.name,
        sc.semester_payment
    FROM
        support_categories sc
    ORDER BY
        id;
END;
$$ LANGUAGE plpgsql;
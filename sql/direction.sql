CREATE OR REPLACE FUNCTION get_directions()
RETURNS TABLE (
    id INT,
    code VARCHAR(8),
    name TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.code,
        d.name
    FROM
        directions d
    ORDER BY
        code;
END;
$$ LANGUAGE plpgsql;
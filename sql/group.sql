CREATE OR REPLACE FUNCTION get_groups()
RETURNS TABLE (
    id INT,
    name VARCHAR(15)
) AS $$
BEGIN
    RETURN QUERY
    SELECT g.id, g.name
    FROM groups g
    ORDER BY g.name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_group(p_name TEXT)
RETURNS VOID AS $$
BEGIN
    INSERT INTO groups (name)
    VALUES (p_name);
END;
$$ LANGUAGE plpgsql;
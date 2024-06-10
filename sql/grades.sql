CREATE OR REPLACE FUNCTION get_student_grades(p_student_id INT)
RETURNS TABLE (
    subject_id INT,
    subject_name TEXT,
    grade INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.name,
        g.grade
    FROM
        subjects s
    JOIN
        grades g
    ON
        s.id = g.subject_id
    WHERE
        g.student_id = p_student_id
    ORDER BY
        s.name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_student_grades(p_student_id INT, p_grades INT[][])
RETURNS VOID AS $$
DECLARE
    i INT;
    v_subject_id INT;
    v_grade INT;
BEGIN
    DELETE FROM grades
    WHERE student_id = p_student_id;

    FOR i IN 1..array_length(p_grades, 1) LOOP
        v_subject_id := p_grades[i][1];
        v_grade := p_grades[i][2];

        IF v_subject_id = 0 THEN
            RETURN;
        END IF;

        INSERT INTO grades (
            student_id,
            subject_id,
            grade
        )
        VALUES (
            p_student_id,
            v_subject_id,
            v_grade
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_other_subjects(p_student_id INT)
RETURNS TABLE (
    id INT,
    name TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT s.id, s.name
    FROM subjects s
    WHERE s.id NOT IN (
        SELECT g.subject_id
        FROM grades g
        WHERE g.student_id = p_student_id
    )
    ORDER BY s.name;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_subject(p_subject_name TEXT)
RETURNS INT AS $$
DECLARE
    v_subject_id INT;
BEGIN
    INSERT INTO subjects (name)
    VALUES (p_subject_name)
    RETURNING id INTO v_subject_id;

    RETURN v_subject_id;
END;
$$ LANGUAGE plpgsql;
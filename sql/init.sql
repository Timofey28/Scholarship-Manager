DO $$
BEGIN

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'penalty') THEN
        CREATE TYPE penalty AS (
            name TEXT,
            amount INT
        );
    END IF;

END
$$;
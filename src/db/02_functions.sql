-- 02_functions.sql
DROP FUNCTION IF EXISTS update_date_modified CASCADE;
CREATE FUNCTION update_date_modified() RETURNS TRIGGER
    LANGUAGE plpgsql AS
$$
BEGIN
    NEW.date_modified := current_timestamp;
RETURN NEW;
END
$$;

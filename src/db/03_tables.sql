-- 03_tables.sql
------------
-- products --
------------
DROP TABLE IF EXISTS products CASCADE;
CREATE TABLE products
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(255) NOT NULL,
    description   TEXT         NOT NULL,
    price         NUMERIC(10, 2) NOT NULL,
    availability  BOOLEAN      NOT NULL,
    category      VARCHAR(255) NOT NULL,
    sale          BOOLEAN      NOT NULL,
    ingredients   TEXT         NOT NULL,
    nutritional_info JSON      NOT NULL,

    date_created  TIMESTAMP    NOT NULL DEFAULT current_timestamp,
    user_created  VARCHAR(255) NOT NULL DEFAULT 'SYSTEM',
    date_modified TIMESTAMP    NOT NULL DEFAULT current_timestamp,
    user_modified VARCHAR(255) NOT NULL DEFAULT 'SYSTEM',
    is_deleted    BOOLEAN      NOT NULL DEFAULT FALSE
);
DROP TRIGGER IF EXISTS trigger_update_date_modified ON products CASCADE;
CREATE TRIGGER trigger_update_date_modified
    BEFORE UPDATE
    ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_date_modified();

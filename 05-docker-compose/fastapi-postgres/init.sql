CREATE TABLE
    IF NOT EXISTS public.items (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT
    );
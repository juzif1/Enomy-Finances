CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
        REFERENCES users(id)
        ON DELETE SET NULL,
    source_currency CHAR(3) NOT NULL,
    target_currency CHAR(3) NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    fee NUMERIC(10,2) NOT NULL,
    result NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE investment_quotes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
        REFERENCES users(id)
        ON DELETE SET NULL,
    investment_type VARCHAR(50) NOT NULL,
    years INTEGER NOT NULL,

    min_value NUMERIC(14,2) NOT NULL,
    max_value NUMERIC(14,2) NOT NULL,

    profit_min NUMERIC(14,2) NOT NULL,
    profit_max NUMERIC(14,2) NOT NULL,

    fees NUMERIC(14,2) NOT NULL,

    tax_min NUMERIC(14,2) NOT NULL,
    tax_max NUMERIC(14,2) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE error_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
        REFERENCES users(id)
        ON DELETE SET NULL,
    error_message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

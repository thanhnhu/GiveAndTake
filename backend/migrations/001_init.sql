CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    email VARCHAR(254) NOT NULL DEFAULT '',
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ NULL
);

CREATE TABLE IF NOT EXISTS authtoken_token (
    key VARCHAR(40) PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    created TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS takers_city (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS api_message (
    id BIGSERIAL PRIMARY KEY,
    subject VARCHAR(200),
    body TEXT
);

CREATE TABLE IF NOT EXISTS takers_taker (
    id UUID PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    number INTEGER UNIQUE NOT NULL,
    city_id BIGINT NOT NULL REFERENCES takers_city(id),
    name VARCHAR(30),
    address VARCHAR(30),
    phone VARCHAR(20),
    description TEXT,
    images JSONB,
    stop_donate BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS takers_giver (
    id UUID PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    number INTEGER UNIQUE NOT NULL,
    city_id BIGINT NOT NULL REFERENCES takers_city(id),
    name VARCHAR(30),
    address VARCHAR(30),
    phone VARCHAR(20),
    description TEXT,
    images JSONB,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS takers_donate (
    id UUID PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    taker_id UUID NOT NULL REFERENCES takers_taker(id) ON DELETE CASCADE,
    donate INTEGER NOT NULL,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_takers_taker_user_id ON takers_taker(user_id);
CREATE INDEX IF NOT EXISTS idx_takers_taker_city_id ON takers_taker(city_id);
CREATE INDEX IF NOT EXISTS idx_takers_giver_user_id ON takers_giver(user_id);
CREATE INDEX IF NOT EXISTS idx_takers_giver_city_id ON takers_giver(city_id);
CREATE INDEX IF NOT EXISTS idx_takers_donate_taker_id ON takers_donate(taker_id);

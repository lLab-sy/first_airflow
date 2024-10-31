CREATE TABLE IF NOT EXISTS rain_per_area (
    id BIGINT PRIMARY KEY,
    at_year INT,
    at_month INT,
    prov_id INT,
    min_rain FLOAT,
    max_rain FLOAT,
    avg_rain FLOAT,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);
CREATE TABLE IF NOT EXISTS weather_hourly (
    city TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    temperature_2m DOUBLE PRECISION
);

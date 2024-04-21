DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
    id INTEGER,
    brand VARCHAR(255),
    model VARCHAR(255),
    color VARCHAR(255),
    registration_date CHAR(7),
    year INTEGER,
    price_in_euro INTEGER,
    power_kw INTEGER,
    power_ps INTEGER,
    transmission_type VARCHAR(255),
    fuel_type VARCHAR(255),
    fuel_consumption_l_100km VARCHAR(255),
    fuel_consumption_g_km VARCHAR(255),
    mileage_in_km FLOAT,
    offer_description TEXT
);


COPY cars FROM '/tmp/autodata.csv' DELIMITER ',' CSV HEADER;

SELECT * FROM cars;
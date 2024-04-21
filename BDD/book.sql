DROP TABLE IF EXISTS books;

CREATE TABLE books (
    book_id INTEGER,
    books_count INTEGER,
    authors TEXT,
    original_publication_year FLOAT,
    title TEXT,
    average_rating NUMERIC,
    ratings_count INTEGER
);

COPY books FROM '/tmp/bookdata.csv' DELIMITER ',' CSV HEADER;

SELECT * FROM books;
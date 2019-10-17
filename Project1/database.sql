--install postgresql from original site. There are instructions
--open terminal
--# service postgresql status (optional to check the status)
--# sudo su postgres
--# psql
--# CREATE DATABASE your_database_name
--# \l (lists all databases)
--# \c your_database_name (selects a database)
--# \dt (shows the tables of a chosen database)
--ctrl + L to clear

--After that copy-paste the following to create tables user, books and reviews.

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    user_password VARCHAR NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    isbn VARCHAR,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INT
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    book_id INT,
    rating INT,
    review_text VARCHAR
);

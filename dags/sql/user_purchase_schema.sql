-- create user_purchase table

CREATE TABLE IF NOT EXISTS user_purchase (
    invoice_no INT NOT NULL,
    stock_code VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    quantity INT NOT NULL,
    invoice_date DATE NOT NULL,
    unit_price REAL NOT NULL,
    customer_id INT NOT NULL,
    country VARCHAR NOT NULL
);

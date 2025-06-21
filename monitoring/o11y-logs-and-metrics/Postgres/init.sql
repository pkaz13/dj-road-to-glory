-- Create the Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Create the Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    CONSTRAINT fk_category
        FOREIGN KEY(category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE
);

-- Add indexes for performance
CREATE INDEX idx_products_category_id ON products(category_id);

-- Populate the database with sample data

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Devices and gadgets'),
('Books', 'Printed and digital books'),
('Clothing', 'Apparel and accessories');

-- Insert sample products
INSERT INTO products (name, description, price, category_id) VALUES
('Laptop', 'A high-performance laptop', 1200.50, 1),
('Smartphone', 'A latest model smartphone', 800.00, 1),
('T-Shirt', 'A cotton t-shirt', 25.99, 3),
('Jeans', 'A pair of blue jeans', 75.00, 3),
('The Great Gatsby', 'A classic novel', 15.75, 2),
('Learning SQL', 'A book for database beginners', 45.50, 2); 
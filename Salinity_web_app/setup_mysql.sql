-- Create DB
CREATE DATABASE IF NOT EXISTS salinity_db;

-- Create user
CREATE USER IF NOT EXISTS 'salinity'@'localhost' IDENTIFIED BY 'admin_pwd';

-- Grant all privileges on the hbnb_dev_db database to the user
GRANT ALL PRIVILEGES ON salinity_db.* TO 'salinity'@'localhost';

-- Grant SELECT privileges on the performance_schema database to the user
GRANT SELECT ON performance_schema.* TO 'salinity'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

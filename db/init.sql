GRANT ALL PRIVILEGES ON captioning.* TO my_user; -- grant privileges for default user

-- create database and table for storing images along with their captions
CREATE DATABASE IF NOT EXISTS captioning;

USE captioning;

CREATE TABLE IF NOT EXISTS Images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    caption VARCHAR(255) NULL,
    model_used VARCHAR(128) NULL,
    image_file LONGBLOB NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

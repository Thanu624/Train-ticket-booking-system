-- Initial Database setup script executed upon Docker MySQL initial start
CREATE DATABASE IF NOT EXISTS train_booking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON train_booking_db.* TO 'train_user'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS vid_conv_dev_db;
CREATE USER IF NOT EXISTS 'vid_user' @'localhost' IDENTIFIED BY 'vid_user';
GRANT ALL PRIVILEGES ON `vid_conv_dev_db`.* TO 'vid_user' @'localhost';
GRANT SELECT ON `performance_schema`.* TO 'vid_user' @'localhost';
FLUSH PRIVILEGES;

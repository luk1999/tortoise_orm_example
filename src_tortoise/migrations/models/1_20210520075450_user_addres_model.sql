-- upgrade --
CREATE TABLE IF NOT EXISTS `useraddress` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `address` VARCHAR(100) NOT NULL,
    `zip_code` VARCHAR(5) NOT NULL,
    `city` VARCHAR(50) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_useraddr_user_2ac2ecdd` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
-- downgrade --
DROP TABLE IF EXISTS `useraddress`;

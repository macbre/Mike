-- This file contains a schema and sample rows for MysqlSource tests
DROP TABLE IF EXISTS `mike_test`;

CREATE TABLE `mike_test` (
  `user_id` int(9) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `user_group` varchar(32) NOT NULL,
  `value` decimal(3,2) NOT NULL DEFAULT 0.0,
  PRIMARY KEY (`user_id`)
) CHARSET=utf8;

INSERT INTO mike_test(name, user_group) VALUES ("Mike", "admin"), ("Macbre", "admin");
INSERT INTO mike_test(name, user_group, value) VALUES ("Monty", "user", "3.456");

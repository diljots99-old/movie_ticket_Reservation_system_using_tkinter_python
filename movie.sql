
DROP TABLE IF EXISTS `users`;

CREATE TABLE IF NOT EXISTS `users` (
  `Sr. No` INTEGER  PRIMARY KEY AUTOINCREMENT,
  `username`  TEXT      NOT NULL,
  `password`  TEXT      NOT NULL,
  `email`     TEXT      NOT NULL,
  `privilege` TEXT      NOT NULL

);



INSERT INTO `users` (`Sr. No`, `username`, `password`, `email`, `privilege`) VALUES
(1, 'admin', 'admin', 'admin@admin.com', 'admin');


DROP TABLE IF EXISTS `users`;

CREATE TABLE IF NOT EXISTS `users` (
  `UID` INTEGER  PRIMARY KEY AUTOINCREMENT,
  `username`  TEXT      NOT NULL,
  `password`  TEXT      NOT NULL,
  `email`     TEXT      NOT NULL,
  `privilege` TEXT      NOT NULL

);



INSERT INTO `users` (`UID`, `username`, `password`, `email`, `privilege`) VALUES
(1, 'admin', 'admin', 'admin@admin.com', 'admin');



DROP TABLE IF EXISTS `movies`;

CREATE TABLE IF NOT EXISTS `movies` (
  `movie_ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
  `title`  TEXT      NOT NULL,
  `overview`  TEXT      NOT NULL,
  `adult`     TEXT      NOT NULL,
  `status`     TEXT      NOT NULL,
  `release_date`     TEXT      NOT NULL,
  `imdb_id`     TEXT      NOT NULL,
  `tmdb_id`     TEXT      UNIQUE NOT NULL,
  `backdrop`     BLOB      NOT NULL,
  `poster`     BLOB      NOT NULL,
  `tagline` TEXT      NOT NULL

);


DROP TABLE IF EXISTS `projections`;

CREATE TABLE IF NOT EXISTS `projections` (
  `projection_ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
  `movie_ID`  INTEGER      NOT NULL,
  `venue`  TEXT      NOT NULL,
  `time`     TEXT      NOT NULL,
  `date`     DATE      NOT NULL,
  FOREIGN KEY (movie_ID)
       REFERENCES movies (movie_ID) 

);
CREATE TABLE `cbb_predictions` (
  `game_date` DATE,
  `game_id` DOUBLE DEFAULT NULL,
  `away_team_full_name` VARCHAR(255),
  `home_team_full_name` VARCHAR(255),
  `prediction_alternate` DOUBLE DEFAULT NULL,
  `prediction_use` DOUBLE DEFAULT NULL,
  `book_line` DOUBLE DEFAULT NULL,
  `edge_v4` DOUBLE DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

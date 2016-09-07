-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  t_id INTEGER REFERENCES tournaments(id)
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  player_one INTEGER REFERENCES players(id) ON DELETE CASCADE,
  player_two INTEGER REFERENCES players(id) ON DELETE CASCADE,
  t_id INTEGER REFERENCES tournaments(id)
);

CREATE TABLE match_results (
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
  winner INTEGER REFERENCES players(id) ON DELETE CASCADE,
  loser INTEGER REFERENCES players(id) ON DELETE CASCADE,
  draw BOOLEAN,
  t_id INTEGER REFERENCES tournaments(id)
);

CREATE TABLE player_match_points(
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
  player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
  t_id INTEGER REFERENCES tournaments(id),
  points INTEGER
);

CREATE TABLE player_byes(
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    bye INTEGER DEFAULT 0,
    t_id INTEGER REFERENCES tournaments(id)
);

CREATE VIEW standings AS
SELECT players.t_id, players.id, players.name,
(SELECT count(*) FROM match_results WHERE players.id = match_results.winner and match_results.draw = FALSE) AS wins,
(SELECT count(*) FROM match_results WHERE players.id = match_results.winner OR players.id = match_results.loser ) AS matches,
(SELECT COALESCE(SUM(points), 0) FROM player_match_points WHERE players.id = player_match_points.player_id) AS total_points,
(SELECT COALESCE(SUM(points), 0) FROM player_match_points WHERE match_id IN (SELECT match_id FROM match_results WHERE loser = players.id) OR match_id IN (SELECT match_id FROM match_results WHERE winner = players.id) and player_id <> players.id) AS omw FROM players ORDER BY wins DESC, omw DESC;

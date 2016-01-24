-- Table definitions for the tournament project.

-- added so if the DB exists, delete it and start from scratch
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- attach the terminal to the tournament db so tables/views can be created
\c tournament;

-- player_id is serialized and the primary key as to ensure unique values
CREATE TABLE players ( player_id SERIAL primary key,
                     name TEXT);

-- the winner_id and loser_id are referenced to the player_id so we know only registered players
-- will be able to be added to the table
CREATE TABLE matches ( winner_id INTEGER references players(player_id),
					 loser_id INTEGER references players(player_id);


-- added the following lines so the consol will output what was created
-- seeing it as it's created will help you catch mistakes
SELECT * from players;
\d players;
SELECT * from matches;
\d matches;

-- wins VIEW is used to count the number of wins per player. Used to simplify later queries.
CREATE VIEW wins as SELECT winner_id as player_id, count(*) as wins from matches group by winner_id;

-- losses view is used to count the number of lossses per player. Used to simplify later queries.
CREATE VIEW losses as SELECT loser_id as player_id, count(*) as losses from matches group by loser_id;

-- joins the wins and losses tables and adds the player names. Used coalesce(x, 0) to ensure that if a player has no losses or wins
-- that the column has a value of '0'
CREATE VIEW w_l as (SELECT players.player_id, players.name, coalesce(wins.wins, 0) as wins, coalesce(losses.losses, 0) as losses
	FROM players
	-- joins the wins view with the players view which adds the names on player_id
	-- left join used so all players are listed regardless of if they have a win
	lEFT JOIN wins
	ON players.player_id=wins.player_id
	-- joins the losses view with the players+wins view join
	LEFT JOIN losses
	on players.player_id=losses.player_id);

-- w_l_m view was created to sum wins and losses on each row. Keeps python from having to do the math and simplifys code.
CREATE VIEW w_l_m as select player_id, name, wins, losses, (wins+losses) as matches from w_l;

-- attach the default db so you can run this command once again without having to manually back out
\c postgres;


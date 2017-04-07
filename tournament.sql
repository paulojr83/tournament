-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--create sequence ro player unique id
CREATE SEQUENCE player_seq;
-- create table for player
CREATE TABLE player(
    "ID" integer NOT NULL DEFAULT  nextval('player_seq'),
    "NAME" varchar(255) NOT NULL,
    PRIMARY KEY ("ID")
)
--create table for matches
CREATE TABLE matches(
    "ID_WINNER" integer NOT NULL,
    "ID_LOSER" integer NOT NULL
)
-- create view for player standings
create view PLAYER_STANDINGS as
select pw."ID" as id1, pw."NAME" as name1,
                    (select count(*) from matches wins where wins."ID_WINNER" = pw."ID") as wins1,
                    (select count(*) from matches where matches."ID_WINNER" = pw."ID" or matches."ID_LOSER" = pw."ID") as matches1
                    from player pw order by wins1

--create view for swiss pairings
create view SWISS_PAIRINGS as
select id1, name1, id2,
(select "NAME" from player where "ID" = sub.id2) as name2 from (
SELECT "ID" as id1
    , "NAME" as name1
    ,LAG("ID", 4) OVER (ORDER BY "ID") as id2
    FROM player) sub where id2 > 0
--create view for test swiss pairings
CREATE view PAIRINGS as
SELECT P_WON."ID" AS id1, P_WON."NAME" as name1, P_LOSE."ID" AS id2, P_LOSE."NAME" as name2
FROM MATCHES A JOIN PLAYER P_WON ON(A."ID_WINNER" = P_WON."ID")
JOIN PLAYER P_LOSE ON(A."ID_LOSER" = P_LOSE."ID")

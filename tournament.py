#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

SELECT_PLAYERS = "SELECT count(*) FROM player;"

INSERT_PLAYER = """INSERT INTO player("NAME") VALUES (%s);"""

INSERT_MATCH = """INSERT INTO matches("ID_WINNER","ID_LOSER") 
                        VALUES (%s, %s);"""

PLAYER_STANDINGS = """SELECT * FROM PLAYER_STANDINGS;"""

SWISS_PAIRINGS = """SELECT * FROM SWISS_PAIRINGS;"""

TRUNCATE_MATCHES = """TRUNCATE matches CASCADE;"""

TRUNCATE_PLAYER = """TRUNCATE player CASCADE;"""

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect(host="64.137.162.204"
                              , database=database_name
                              , user="postgres"
                              , password="12qw")
        cursor = db.cursor()
        return db, cursor
    except:
        print "I am unable to connect to the database"

def deleteMatches():
    """Remove all the match records from the database."""
    print "deleteMatches"
    try:
        db, cursor = connect()
        cursor.execute(TRUNCATE_MATCHES)
        db.commit()
        closeConnCur(db, cursor)

    except psycopg2.Error as e:
        print e.pgerror

def deletePlayers():
    """Remove all the player records from the database."""
    print "deletePlayers"
    try:
        db, cursor = connect()
        cursor.execute(TRUNCATE_PLAYER)
        db.commit()
        closeConnCur(db, cursor)

    except psycopg2.Error as e:
        print e.pgerror

"""Returns the number of players currently registered."""
def countPlayers():
    print "countPlayers"
    try:
        db, cursor = connect()
        cursor.execute(SELECT_PLAYERS)
        count = cursor.fetchone()[0]
        closeConnCur(db, cursor)
        return int(count)
    except psycopg2.Error as e:
        print e.pgerror

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    print "registerPlayer"
    try:
        parameter = (name,)
        db, cursor = connect()
        cursor.execute(INSERT_PLAYER,parameter)
        db.commit()
        closeConnCur(db, cursor)

    except psycopg2.Error as e:
        print e.pgerror

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    print "playerStandings"
    try:
        db, cursor = connect()
        cursor.execute(PLAYER_STANDINGS)
        standings = cursor.fetchall()
        closeConnCur(db, cursor)
        return standings

    except psycopg2.Error as e:
        print e.pgerror

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    print "reportMatch"
    try:
        parameters = (winner,loser)
        db, cursor = connect()
        cursor.execute(INSERT_MATCH,parameters)
        db.commit()
        closeConnCur(db, cursor)

    except psycopg2.Error as e:
        print e.pgerror
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    print "swissPairings"
    try:
        db, cursor = connect()
        cursor.execute(SWISS_PAIRINGS)
        standings = cursor.fetchall()
        closeConnCur(db, cursor)
        return standings

    except psycopg2.Error as e:
        print e.pgerror

def closeConnCur(conn, cur):
    if conn:
        conn.close()
    if cur:
        cur.close()
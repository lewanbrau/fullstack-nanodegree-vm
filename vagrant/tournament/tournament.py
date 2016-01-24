#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()

    # deletes all records from the matches table
    query = "DELETE FROM matches;"
    c.execute(query)
    conn.commit()
    conn.close()
    

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()

    # deletes all rows from the players table
    query = "DELETE FROM players"
    c.execute(query)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()

    # counts the rows in players. Doesn't matter if names are the same
    # since the player_id is forced unique from the players table
    query = "SELECT COUNT(*) FROM players"
    c.execute(query)
    count = c.fetchall()
    conn.close()
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()

    # Simple insert into the players table. player_id is serialized
    # automatically by the db
    c.execute("INSERT INTO players (name) values (%s)",
        (name,))
    conn.commit()
    conn.close()


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
    conn = connect()
    c = conn.cursor()

    # Pulls data from the set w_l_m view created when the tournament.sql is run.
    # This view does all the assembly for you so you just need to specify which
    # select which fields wanted from w_l_m and the sorting params
    query = "SELECT player_id, name, wins, matches FROM w_l_m ORDER BY wins DESC"
    c.execute(query)
    records = c.fetchall()
    conn.close()
    return records



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()

    # Insert the values supplied by the function parameters into the 
    # matches table
    c.execute("insert into matches (winner_id, loser_id) values (%s, %s)",
                (winner, loser))
    conn.commit()
    conn.close()

 
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
    conn = connect()
    c = conn.cursor()

    # Pulls data with just player_id and name in order of wins
    query = "SELECT player_id, name FROM w_l_m ORDER BY wins DESC"
    c.execute(query)
    # store the results of the query in a variable
    records = c.fetchall()

    # setup the variables needed in the while loop
    l = len(records)
    i = 0
    matches = []

    # Uses the ordered tuple output of the above query to
    # construct paired matches based on people with similar
    # records
    while i < l:
        matches = matches + [(records[i] + records[i+1])]
        i = i + 2
    return matches


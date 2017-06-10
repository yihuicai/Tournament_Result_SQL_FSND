#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from functools import wraps

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        return db
    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN perhaps exit the program
        raise e

def sql_action(actions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            conn=connect()
            cursor=conn.cursor()
            ret=None
            for action in actions:
                cursor.execute(action)
                if action[:6].find('SELECT')!=-1:
                    val=cursor.fetchall()
                    ret=f(val)
                else:
                    f(*args, **kwargs)
            conn.commit()
            conn.close()
            return ret
        return decorated_function
    return decorator


def sql_action2(actions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            conn=connect()
            cursor=conn.cursor()
            ret=None
            for action in actions:
                cursor.execute(action[0], action[1])
                if action[0].find('SELECT')!=-1:
                    val=cursor.fetchall()
                    ret=f(val)
                else:
                    ret=f(*args, **kwargs)
            conn.commit()
            conn.close()
            return ret
        return decorated_function
    return decorator

def deleteMatches():
    @sql_action([("DELETE FROM result;") ])
    def delete_m():
        """Remove all the match records from the database."""
        return
    delete_m()
    return

def deletePlayers():
    @sql_action([("DELETE FROM player;")])
    def delete_p():
        """Remove all the player records from the database."""
        return
    delete_p()
    return

def countPlayers():
    @sql_action([("SELECT count(*) as num FROM player;")])
    def count_p(val):
        """Returns the number of players currently registered."""
        nums = val
        return int(nums[0][0])
    re=count_p()
    return re


def registerPlayer(name):
    @sql_action2([("INSERT INTO player (name) VALUES (%s); ", (name,))])
    def register_p():
        """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
        """
        return
    register_p()
    return


def playerStandings():
    @sql_action([("DROP VIEW IF EXISTS matches;"),
                 ("""CREATE VIEW matches AS SELECT total.id AS id, COUNT(total.id) AS matches FROM (SELECT winner AS id FROM result
                    UNION ALL SELECT loser AS id FROM result) 
                    AS total GROUP BY total.id ;"""),
                    ("""SELECT player.id, player.name, COALESCE(wins.wins,0), COALESCE(matches.matches,0) FROM player 
                    LEFT OUTER JOIN (SELECT result.winner AS id, count(result.winner) AS wins FROM result GROUP BY result.winner) AS wins ON player.id = wins.id
                    LEFT OUTER JOIN matches ON player.id = matches.id ORDER BY 3,4 DESC; """)])   
    def play_s(val=None):
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
        return val
    ret=play_s()
    return ret
    
    


def reportMatch(winner, loser):
    @sql_action2([("INSERT INTO result(winner,loser) VALUES (%s, %s); ", (winner, loser) )])
    def report_m():
        """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
        return
    ret = report_m()
    return ret
 
 
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
    standing=playerStandings()
    li=[]
    for i in range (0, len(standing), 2):
        li.append((standing[i][0], standing[i][1], standing[i+1][0], standing[i+1][1]))
    return li
    

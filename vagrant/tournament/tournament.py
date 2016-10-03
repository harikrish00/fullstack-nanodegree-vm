#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import math
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def create_tournament(name=''):
    """Create a new tournament for conducting mathces"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into tournaments (name) values (%s) returning id", (name,))
    t_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return t_id

def delete_tournament():
    """Remove all the records from the tournaments."""
    conn = connect()
    cursor = conn.cursor()
    query = "delete from tournaments"
    cursor.execute(query);
    conn.commit()
    conn.close()

def delete_table(t_id, table_name):
    """Remove all the records from the given table."""
    conn = connect()
    cursor = conn.cursor()
    query = "delete from %s where t_id=%d" % (table_name, t_id)
    cursor.execute(query);
    conn.commit()
    conn.close()

def count_players(t_id):
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) from players where t_id=%d" % t_id)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def player_with_byes(t_id):
    """Returns all the players who have recieved bye"""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select * from player_byes where t_id=%d" % t_id)
    player_byes = cursor.fetchall()
    conn.close()
    return player_byes

def register_player(t_id, name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      t_id: tournament id where the player is registering to
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    sql = "insert into players (t_id, name) values (%s, %s)"
    cursor.execute(sql, (t_id, name))
    conn.commit()
    conn.close()


def player_match_points(t_id, match_id):
    """Returns players points for a particular match

    Player is assigned points for each match played based on the outcome of the match.
    Those points are recorded in this database, and this function fetches the points
    for particular match given

    Args:
      t_id: tournament id where player belongs to
      match_id: id of the match
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select * from player_match_points where t_id=%d and match_id=%d" % (t_id, match_id))
    points = cursor.fetchall()
    conn.close()
    return points

def player_standings(t_id):
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
    cursor = conn.cursor()
    cursor.execute("select * from standings where t_id=%d" % t_id)
    standings = cursor.fetchall()
    conn.close()
    return standings

def report_match(t_id, match_id, winner, loser, draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: A boolean, to report a match draw. Carries default value of False.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into match_results(t_id, match_id, winner, loser, draw) \
                        values(%d, %d, %d, %d, %s)" % (t_id, match_id, winner, loser, draw))

    # If match is draw then assign one point for each player
    if draw == True:
        winner_points = 1
        loser_points = 1
    else:
        # if match is not a draw then winner gets 3 points
        winner_points = 3
        loser_points = 0

    cursor.execute("insert into player_match_points (t_id, match_id, player_id, points) \
                        values (%d, %d, %d, %d)" % (t_id, match_id, winner, winner_points))
    cursor.execute("insert into player_match_points (t_id, match_id, player_id, points) \
                        values (%d, %d, %d, %d)" % (t_id, match_id, loser, loser_points))
    conn.commit()
    conn.close()

def player_with_no_bye(t_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select players.id from players, player_byes where player_byes.player_id <> players.id and t_id=%d" % t_id)
    player = cursor.fetchone()[0]
    conn.close()
    return player

def report_bye(t_id, player_id):
    """ Records bye for a user when there are odd number of players registered for the tournament """

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches (t_id, player_one) values(%d, %d)" % (t_id,player_id))
    conn.commit()
    cursor.execute("select max(id) from matches")
    match_id = cursor.fetchone()[0]
    points = 3
    bye = 1
    cursor.execute("insert into player_match_points (t_id, match_id, player_id, points) \
                        values(%d, %d, %d, %d)" % (t_id, match_id, player_id, points))
    cursor.execute("insert into player_byes (t_id, player_id, bye) \
                        values(%d, %d, %d)" % (t_id, player_id, bye))
    conn.commit()
    conn.close()

def swiss_pairings(t_id):
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
    standings = player_standings(t_id)
    total_players = len(standings)
    game_pairs = []
    #standings are always ordered by wins descending, and if the first player
    #in the standings has 0 matches then its the first round
    if standings[0][4] == 0:
        #for the first round generate game pairs randomly
        order = get_random_pairs(0, total_players)
        # check if even numbers of players are there
        if not total_players % 2 == 0:
            #in case of even numbers of players report bye for one player
            report_bye(t_id, standings[order[-1]][1])
            del order[-1]
    #other than the initial round, generate the game pair based on standings
    else:
        order = [i for i in range(total_players)]
        matches = get_matches(t_id)
        i = 0
        matches = get_sorted_matches(matches)

        for i in range(0,total_players - 1,2):
            pair = (standings[i][1],standings[i+1][1])
            if sorted(pair) in matches:
                temp = order[i+1]
                order[i+1] = order[i+2]
                order[i+2] = temp
        if not total_players % 2 == 0:
            player = player_with_no_bye(t_id)
            for i in range(total_players-1,0,-1):
                if player == standings[i][1]:
                    report_bye(t_id, player)
                    del order[i]
                    break
    game_pairs = get_game_pairs(order, standings)
    create_matches(t_id, game_pairs)
    return game_pairs

def create_matches(t_id, game_pairs):
    """Create the matches after a swiss pairing is generated"""
    conn = connect()
    cursor = conn.cursor()
    for pair in game_pairs:
        cursor.execute("insert into matches (t_id, player_one, player_two) values(%d, %d, %d)" % (t_id, pair[0], pair[2]))
        conn.commit()
    conn.close()

def get_sorted_matches(matches):
    """Sort the matches in ascending order for comparison"""
    sorted_matches = []
    for match in matches:
        sorted_matches.append(sorted(match))
    return sorted_matches

def get_matches(t_id):
    """Returns all the matches scheduled to be played"""
    conn = connect()
    c = conn.cursor()
    c.execute("select * from matches where t_id=%d" % t_id)
    matches = c.fetchall()
    conn.close()
    return matches

def get_game_pairs(order, standings):
    """Generate game pairs based on the standings for subsequent matches"""
    game_pairs = [(standings[i][1], standings[i][2]) for i in order]
    return [game_pairs[i] + game_pairs[i+1] for i in range(0, len(order), 2)]

def get_random_pairs(low,high):
    """Genereate a radom order for initial pairings"""
    return random.sample(xrange(high),high)

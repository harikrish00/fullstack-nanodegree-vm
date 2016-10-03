#!/usr/bin/env python

from tournament import *
import math

def test_rematch_is_prevented():
    """
    Test for rematch between player is prevented
    """
    t_id = create_tournament('test')
    register_player(t_id, 'Cheryl Shakin')
    register_player(t_id, 'Tena Stone')
    register_player(t_id, 'Norma Chapa')
    register_player(t_id, 'Theresa Fisher')
    register_player(t_id, 'Julio Thompson')
    register_player(t_id, 'Frank Pabon')
    register_player(t_id, 'Diana Twiford')
    register_player(t_id, 'Chad Mason')
    swiss_pairings(t_id)
    rematch = False
    for i in range(3):
        matches = get_matches(t_id)[-4:]
        for match in matches:
            report_match(match[3],match[0],match[1],match[2])
        swiss_pairings(t_id)
        matches = get_matches(t_id)
        if not len(matches) == len(set(matches)):
            rematch = True
    if rematch:
        raise ValueError(
            "Rematch between players should be prevented, and total rematch occurred is %d" % (len(matches)- len(set(matches))))
    print "1. Rematch between players is prevented. Good Job!"
    delete_tournament()

def test_assign_bye_for_odd_number_of_players():
    t_id = create_tournament('test')
    register_player(t_id, 'Cheryl Shakin')
    register_player(t_id, 'Tena Stone')
    register_player(t_id, 'Norma Chapa')
    register_player(t_id, 'Theresa Fisher')
    register_player(t_id, 'Julio Thompson')
    swiss_pairings(t_id)
    player_byes = player_with_byes(t_id)
    if not len(player_byes) == 1:
        raise ValueError(
            "A player should be assigned a bye when odd number of players registered, total bye assigned is 0")
    print "2. A player is assigned a bye when odd number of players are registered"
    standings = player_standings(t_id)
    for item in standings:
        if item[1] == player_byes[0][0]:
            if not item[5] == 3 and item[4] == 1:
                raise ValueError(
                    "A bye should be counted as free win and 3 points should be assigned to the user, total points %d" % item[5])
    print "3. A bye is counted as free win and player is assigned 3 points"
    delete_tournament()

def test_support_for_match_draw():
    t_id = create_tournament('test')
    register_player(t_id, 'Cheryl Shakin')
    register_player(t_id, 'Tena Stone')
    register_player(t_id, 'Norma Chapa')
    register_player(t_id, 'Theresa Fisher')
    swiss_pairings(t_id)
    matches = get_matches(t_id)
    match = matches[0]
    report_match(match[3],match[0],match[1],match[2],draw=True)
    points = player_match_points(match[3],match[0])
    if len(points) == 2 and points[0][4] == 1 and points[1][4] == 1:
        print "4. Support for match draw is implemented, each player is given 1 points"
    else:
        raise ValueError(
            "Support for match draw should be supported, and each player should be given 1 points each, but the points for player 1 is %d and player 2 is %d" % (points[0][4],points[1][4]))
    delete_tournament()

def test_more_than_one_tournament_is_supported():
    tid1 = create_tournament("tournament1")
    tid2 = create_tournament("tournament2")
    t1_players = ['Alison George','Michelle G']
    t2_players = ['Hillary C','Bill Mayer']
    for p in t1_players:
        register_player(tid1,p)
    for p in t2_players:
        register_player(tid2,p)

    for player in player_standings(tid1):
        if not player[2] in t1_players:
            raise ValueError(
                "Registered players are not found in the tournament")
            player_foudn = False

    for player in player_standings(tid2):
        if not player[2] in t2_players:
            raise ValueError(
                "Registered players are not found in the tournament")
            player_foudn = False
    print "5. Supports more than one tournament, and players registering for particular tournament belongs to the same tournament"
    delete_tournament()

if __name__ == '__main__':
    test_rematch_is_prevented()
    test_assign_bye_for_odd_number_of_players()
    test_support_for_match_draw()
    test_more_than_one_tournament_is_supported()
    print "Success!  All tests pass!"

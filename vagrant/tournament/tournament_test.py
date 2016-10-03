#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *
import tournament_extra_credit_test

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    t_id =  create_tournament("test")
    c = count_players(t_id)
    if c == '0':
        raise TypeError(
            "count_players should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, count_players should return zero.")
    print "1. count_players() returns 0 after initial deletePlayers() execution."
    register_player(t_id, "Chandra Nalaar")
    c = count_players(t_id)
    if c != 1:
        raise ValueError(
            "After one player registers, count_players() should be 1. Got {c}".format(c=c))
    print "2. count_players() returns 1 after one player is registered."
    register_player(t_id, "Jace Beleren")
    c = count_players(t_id)
    if c != 2:
        raise ValueError(
            "After two players register, count_players() should be 2. Got {c}".format(c=c))
    print "3. count_players() returns 2 after two players are registered."
    delete_table(t_id, 'players')
    c = count_players(t_id)
    if c != 0:
        raise ValueError(
            "After deletion, count_players should return zero.")
    print "4. count_players() returns zero after registered players are deleted.\n5. Player records successfully deleted."
    delete_tournament()

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    t_id = create_tournament("test")
    register_player(t_id, "Melpomene Murray")
    register_player(t_id, "Randy Schwartz")
    standings = player_standings(t_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in player_standings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 7:
        raise ValueError("Each player_standings row should have seven columns.")
    [(tid1, id1, name1, wins1, matches1, points1, omw1), (tid2, id2, name2, wins2, matches2, points2, omw2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0 or points1 != 0 or points2 != 0:
        raise ValueError(
            "Newly registered players should have no matches, wins or points.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."
    delete_tournament()

def testreport_matches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    t_id = create_tournament("test")
    register_player(t_id, "Bruno Walton")
    register_player(t_id, "Boots O'Neal")
    register_player(t_id, "Cathy Burton")
    register_player(t_id, "Diane Grant")
    swiss_pairings(t_id)
    matches = get_matches(t_id)

    [match1,id1,id2] = [matches[0][0], matches[0][1], matches[0][2]]
    [match2,id3,id4] = [matches[1][0],matches[1][1], matches[1][2]]
    report_match(t_id, match1, id1, id2)
    report_match(t_id, match2, id3, id4)
    standings = player_standings(t_id)
    for (t, i, n, w, m, p, o) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    delete_tournament()

    # delete_table('matches')
    # standings = player_standings()
    # if len(standings) != 4:
    #     raise ValueError("Match deletion should not change number of players in standings.")
    # for (i, n, w, m, p, o) in standings:
    #     if m != 0:
    #         raise ValueError("After deleting matches, players should have zero matches recorded.")
    #     if w != 0:
    #         raise ValueError("After deleting matches, players should have zero wins recorded.")
    # print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    t_id = create_tournament("test")
    register_player(t_id, "Twilight Sparkle")
    register_player(t_id, "Fluttershy")
    register_player(t_id, "Applejack")
    register_player(t_id, "Pinkie Pie")
    register_player(t_id, "Rarity")
    register_player(t_id, "Rainbow Dash")
    register_player(t_id, "Princess Celestia")
    register_player(t_id, "Princess Luna")
    pairings = swiss_pairings(t_id)
    matches = get_matches(t_id)
    [match1,id1,id2] = [matches[0][0], matches[0][1], matches[0][2]]
    [match2,id3,id4] = [matches[1][0], matches[1][1],matches[1][2]]
    [match3,id5,id6] = [matches[2][0], matches[2][1], matches[2][2]]
    [match4,id7,id8] = [matches[3][0], matches[3][1],matches[3][2]]

    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    report_match(t_id, match1, id1, id2)
    report_match(t_id, match2, id3, id4)
    report_match(t_id, match3, id5, id6)
    report_match(t_id, match4, id7, id8)
    pairings = swiss_pairings(t_id)
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are properly paired."
    delete_tournament()

if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testreport_matches()
    testPairings()
    print '-' * 20
    print "Extra Credit Tests"
    print '-' * 20
    ec = tournament_extra_credit_test
    ec.test_rematch_is_prevented()
    ec.test_assign_bye_for_odd_number_of_players()
    ec.test_support_for_match_draw()
    ec.test_more_than_one_tournament_is_supported()
    print "Success!  All tests pass!"

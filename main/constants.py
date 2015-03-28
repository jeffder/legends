# AFL/Legends for games and ladders
AFL = 'AFL'
LEGENDS = 'Legends'


# Prize categories
class PrizeCategories(object):
    categories =   \
        PREMIER, RUNNER_UP, MINOR_PREMIER, WOODEN_SPOON, COLEMAN, BROWNLOW,   \
        MARGINS, CROWDS, HIGH_SEASON, HIGH_ROUND =   \
        'Premier', 'Runner Up', 'Minor Premier', 'Wooden Spoon', 'Coleman',   \
        'Brownlow', 'Margins', 'Crowds', 'High Season', 'High Round'


class Round(object):
    statuses = SCHEDULED, PROVISIONAL, FINAL = \
        'Scheduled', 'Provisional', 'Final'

    # Fees are due by the beginning of this round
    FEES_BY = 'Round 3'


class Game(object):
    statuses = SCHEDULED, PROVISIONAL, FINAL =   \
        'Scheduled', 'Provisional', 'Final'


class TipPoints(object):
    # Points per correct winner
    WINNER = 6

    # Bonus points for tipping every winner in a 9 game round
    WINNERS_BONUS_GAME_COUNT = 9
    WINNERS_BONUS = 10

    # Points per difference from actual crowd
    CROWDS = {
        0: 8,
        1000: 4,
        2000: 3,
        3000: 2,
        4000: 1
    }

    # Points per difference from actual margin (must tip winner)
    MARGINS = {
        0: 20,
        1: 18,
        2: 16,
        3: 14,
        4: 12,
        5: 10,
        6: 9,
        7: 8,
        8: 7,
        9: 6,
        10: 5,
        11: 4,
        12: 3,
        13: 2,
        14: 1
    }

    # Points for Supercoach ranking position in game
    SUPERCOACH = {
        1: 10,
        2: 8,
        3: 6,
        4: 4,
        5: 2,
    }


class LadderPoints(object):
    """
    Points for AFL and Legends ladders
    """
    # Points for win
    WIN_POINTS = 4

    # Points for draw
    DRAW_POINTS = 2


class Supercoach(object):
    """
    Supercoach related constants.
    """
    tips_count = SC_COUNT_HOME_AWAY, SC_COUNT_FINALS, SC_COUNT_GRAND_FINAL = \
        1, 5, 7

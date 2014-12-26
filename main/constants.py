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
    statuses = SCHEDULED, PROVISIONAL, FINAL =   \
        'Scheduled', 'Provisional', 'Final'

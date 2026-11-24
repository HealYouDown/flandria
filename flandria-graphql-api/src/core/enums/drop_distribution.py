import enum


class DropDistribution(enum.Enum):
    # Dropped into the loot box of the current looter
    DEFAULT = 0
    # Every eligible party member receives the full amount
    PER_PLAYER = 1
    # The amount is split across eligible party members (capped by max_per_player)
    SHARED = 2

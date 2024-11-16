import enum


class ItemFlag(enum.Enum):
    # 'Cash' or 'Event' on Accessories, Hats, Dresses
    NO_FLAG = 0
    EVENT = 1
    CASH = 2

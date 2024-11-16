import enum


class MonsterMessageTrigger(enum.Enum):
    IDLE = 0
    ATTACK = 1
    DAMAGE = 2
    CRITICAL = 3
    DIE = 4
    REGENERATION = 5

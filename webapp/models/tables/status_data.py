from webapp.extensions import db
from webapp.models.enums import CharacterClass


class StatusData(db.Model):
    """
    Includes data for all status points (up to ~1000).

    point_type can be either the listed columns (max_hp, max_mp ...)
    or level.
    If it is level, the values are the base values.
    For all other types, just the increment is stored.
    (e.g. from 5 to 6 con, you get +30 max hp).

    level is either the real level for the character or the level of the
    status point (e.g. 300, if you have 300 points invested in con).
    """
    __tablename__ = "status_data"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    point_type = db.Column(db.String(32), nullable=False)
    character_class = db.Column(db.Enum(CharacterClass), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    max_hp = db.Column(db.Integer, nullable=False)
    max_mp = db.Column(db.Integer, nullable=False)
    avoidance = db.Column(db.Integer, nullable=False)

    melee_min_attack = db.Column(db.Integer, nullable=False)
    melee_max_attack = db.Column(db.Integer, nullable=False)
    melee_hitrate = db.Column(db.Integer, nullable=False)
    melee_critical_rate = db.Column(db.Integer, nullable=False)

    range_min_attack = db.Column(db.Integer, nullable=False)
    range_max_attack = db.Column(db.Integer, nullable=False)
    range_hitrate = db.Column(db.Integer, nullable=False)
    range_critical_rate = db.Column(db.Integer, nullable=False)

    magic_min_attack = db.Column(db.Integer, nullable=False)
    magic_max_attack = db.Column(db.Integer, nullable=False)
    magic_hitrate = db.Column(db.Integer, nullable=False)
    magic_critical_rate = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        # Dict only contains values that are non-zero
        fields = [
            "max_hp", "max_mp", "avoidance",
            "melee_min_attack", "melee_max_attack", "melee_hitrate",
            "melee_critical_rate",
            "range_min_attack", "range_max_attack", "range_hitrate",
            "range_critical_rate",
            "magic_min_attack", "magic_max_attack", "magic_hitrate",
            "magic_critical_rate",
        ]

        dic = {
            "level": self.level,
            # "point_type": self.point_type,
            # "character_class": self.character_class.to_dict(),
        }

        for field in fields:
            value = getattr(self, field)
            if value != 0:
                dic[field] = value

        return dic

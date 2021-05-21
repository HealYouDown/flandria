from webapp.extensions import db


class MapPoint(db.Model):
    __tablename__ = "map_point"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    map_code = db.Column(db.String(32), db.ForeignKey("map.code"),
                         nullable=False)
    map = db.relationship("Map", foreign_keys=[map_code], viewonly=True,)

    monster_code = db.Column(db.String(32), db.ForeignKey("monster.code"),
                             nullable=False)
    monster = db.relationship("Monster", foreign_keys=[monster_code], viewonly=True,)

    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    z = db.Column(db.Integer, nullable=False)

    def to_dict(
        self,
        monster_dict: bool = False,
        map_dict: bool = False,
    ) -> dict:
        if monster_dict:
            return {
                "monster": self.monster.to_dict(minimal=True),
                "pos": {
                    "x": self.x,
                    "y": self.y,
                    "z": self.z,
                },
            }

        elif map_dict:
            return {
                "map": self.map.to_dict(minimal=True),
                "pos": {
                    "x": self.x,
                    "y": self.y,
                    "z": self.z,
                },
            }

        return {
            "map": self.map.to_dict(minimal=True),
            "monster": self.monster.to_dict(minimal=True),
            "pos": {
                "x": self.x,
                "y": self.y,
                "z": self.z,
            },
        }

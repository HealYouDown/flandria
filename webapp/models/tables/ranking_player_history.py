from webapp.extensions import db
from webapp.models.enums import CharacterClass, Server
from webapp.utils import get_utc_now


class RankingPlayerHistory(db.Model):
    __tablename__ = "ranking_player_history"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server = db.Column(db.Enum(Server), nullable=False)
    name = db.Column(db.String(16), nullable=False)

    previous_level_land = db.Column(db.Integer)
    new_level_land = db.Column(db.Integer)

    previous_level_sea = db.Column(db.Integer)
    new_level_sea = db.Column(db.Integer)

    previous_character_class = db.Column(db.Enum(CharacterClass))
    new_character_class = db.Column(db.Enum(CharacterClass))

    previous_guild = db.Column(db.String(16))
    new_guild = db.Column(db.String(16))

    inserted_at = db.Column(db.DateTime, default=get_utc_now)

    def to_dict(self) -> dict:
        changes = {}

        if self.previous_level_land:
            changes["previous_level_land"] = self.previous_level_land
            changes["new_level_land"] = self.new_level_land

        if self.previous_level_sea:
            changes["previous_level_sea"] = self.previous_level_sea
            changes["new_level_sea"] = self.new_level_sea

        if self.previous_character_class:
            changes["previous_character_class"] = (
                self.previous_character_class.to_dict())
            changes["new_character_class"] = self.new_character_class.to_dict()

        if self.previous_guild or self.new_guild:
            changes["previous_guild"] = self.previous_guild
            changes["new_guild"] = self.new_guild

        return {
            "inserted_at": str(self.inserted_at),
            "changes": changes,
        }

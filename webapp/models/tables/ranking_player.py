from webapp.extensions import db
from webapp.models.enums import CharacterClass, Server
from webapp.utils import get_utc_now


class RankingPlayer(db.Model):
    __tablename__ = "ranking_player"

    # Unique key consists of servername_username, both case insensitive
    # e.g. bergruen_Shadow or luxplena_Shadow
    # Used to filter later
    composite_key_string = db.Column(db.String(32), nullable=False)

    server = db.Column(db.Enum(Server), nullable=False, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True,
                     primary_key=True)

    rank = db.Column(db.Integer, nullable=False)
    guild = db.Column(db.String(32))
    character_class = db.Column(db.Enum(CharacterClass), nullable=False)

    level_land = db.Column(db.Integer, nullable=False)
    level_sea = db.Column(db.Integer, nullable=False)

    updated_at = db.Column(db.DateTime, onupdate=get_utc_now)
    indexed_at = db.Column(db.DateTime, default=get_utc_now)

    history = db.relationship(
        "RankingPlayerHistory",
        primaryjoin=(
            "and_("
            "foreign(RankingPlayerHistory.server) == RankingPlayer.server,"
            "foreign(RankingPlayerHistory.name) == RankingPlayer.name"
            ")"
        ),
        order_by="RankingPlayerHistory.inserted_at.desc()",
        viewonly=True,
    )

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "server": self.server.to_dict(),
            "name": self.name,
            "rank": self.rank,
            "guild": self.guild,
            "character_class": self.character_class.to_dict(),
            "level_land": self.level_land,
            "level_sea": self.level_sea,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "history": [history.to_dict() for history in self.history],
            "updated_at": str(self.updated_at) if self.updated_at else None,
            "indexed_at": str(self.indexed_at),
        }

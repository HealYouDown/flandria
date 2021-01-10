from flask_restx import Resource
from sqlalchemy import func
from webapp.api.utils import get_url_parameter
from webapp.extensions import db
from webapp.models import RankingPlayer
from webapp.models.enums import CharacterClass, Server


class RankingStatisticsView(Resource):
    def get(self):
        min_level_land = get_url_parameter("min_level_land", int, 1)

        resp = {
            "character_counts": self._get_character_counts(min_level_land)
        }

        return resp, 200

    def _get_character_counts(
        self,
        min_level_land: int
    ) -> dict:
        data = (
            db.session.query(
                RankingPlayer.server,
                RankingPlayer.character_class,
                func.count(RankingPlayer.character_class)
            ).filter(
                RankingPlayer.level_land >= min_level_land,
            ).group_by(
                RankingPlayer.server,
                RankingPlayer.character_class
            ).order_by(
                # this forces the result to go (ber, lux, ber, lux)
                # for each class
                RankingPlayer.character_class,
            ).all()
        )

        # Responses to store all counts
        character_counts = []
        total_count_lux = 0
        total_count_ber = 0

        # For each server, count and calculate all different
        # counts of classes
        for character_class in CharacterClass:
            # Fill out missing data because count in database
            # result in 0
            ber_data = [entry for entry in data
                        if entry[0] == Server.bergruen
                        and entry[1] == character_class]
            if not ber_data:
                ber_data.append([Server.bergruen, character_class, 0])

            lux_data = [entry for entry in data
                        if entry[0] == Server.luxplena
                        and entry[1] == character_class]
            if not lux_data:
                lux_data.append([Server.luxplena, character_class, 0])

            ber_count = ber_data[0][2]
            lux_count = lux_data[0][2]

            character_counts.append({
                "label": character_class.to_dict()["name"],
                "class": character_class.to_dict(),
                "Bergruen": ber_count,
                "LuxPlena": lux_count,
            })

            total_count_ber += ber_count
            total_count_lux += lux_count

        return {
            "counts": character_counts,
            "total_count_lux": total_count_lux,
            "total_count_ber": total_count_ber,
        }

from flask_restx import Resource, abort
from webapp.extensions import cache
from webapp.models import PlayerSkill

CLASSNAME_TO_SKILL_CODES = {
    "noble": [
        "cp002300", "ck500000", "cp008700", "cp006800", "cp010200", "cp002400",
        "cp006200", "cp008300", "cp006000", "cp002600", "cp006100", "cp008200",
        "cp002900", "cp006400", "cp002500", "cp006300", "cp008800", "cp008900",
        "cp006700", "cp002800", "cp006600", "cp009100", "cp007000", "cp002700",
        "cp003000", "cp006500", "cp006900", "cp008400", "cp008600", "cp008500"
    ],
    "explorer": [
        "ck500000", "ck000700", "ck005200", "ck008700", "ck009000", "ck005800",
        "ck009100", "ck005300", "ck008500", "ck000800", "ck001000", "ck000900",
        "ck008400", "ck008800", "ck005900", "ck005400", "ck001100", "ck001200",
        "ck009200", "ck008000", "ck008300", "ck007900", "ck001500", "ck001300",
        "ck005700", "ck005500", "ck008100", "ck005600", "ck008600"
    ],
    "mercenary": [
        "ck500000", "ck004600", "ck000400", "ck008900", "ck000100", "ck004700",
        "ck004200", "ck004400", "ck007000", "ck003900", "ck000000", "ck004000",
        "ck004300", "ck004500", "ck007600", "ck007400", "ck004100", "ck004800",
        "ck000500", "ck007100", "ck004900", "ck005100", "ck000300", "ck005000",
        "ck007500", "ck007800", "ck000200", "ck000600", "ck007700", "ck007200"
    ],
    "saint": [
        "cp003500", "cp007700", "cp007600", "cp009600", "cp003100", "cp008000",
        "cp003200", "cp007100", "cp009300", "cp009200", "cp007800", "cp003800",
        "cp003400", "cp003600", "cp009400", "cp007200", "cp007900", "cp003300",
        "cp009500", "cp003700", "cp007300", "cp007400", "cp009800", "cp009700",
        "cp010100", "ck500000", "cp010300", "cp008100", "cp007500", "cp009900"
    ],
    "ship": [
        "sksinso00", "skpogye00", "skjojun00", "skwehyu00", "skpokba00",
        "skchain00", "skadomi00", "skhwaks00", "skstst000", "skgwant00",
        "skrange00", "skunpro00", "skgyeon00", "skjilju00", "skwinds00",
        "skpagoe00", "skransh00", "skadest00", "skyeonb00", "skgeunj00",
        "skangae00", "skhide000", "skdarks00", "skchung00", "skload000",
        "skflash00", "skavoid00", "skjaesa00", "skhambo00", "sksiles00",
        "skchiyu00", "skshipr00", "skchund00", "skendur00", "sksick000",
        "skspecs00", "skturn000", "skyuck000", "skjunja00", "skgyeol00",
        "skjunso00", "skshotm00", "skdouca00", "sklimit00",
    ]
}


class PlannerView(Resource):
    def get(self, classname: str):
        if classname not in CLASSNAME_TO_SKILL_CODES:
            abort(404)

        resp = self._get_response(classname)

        return resp, 200

    @cache.memoize(timeout=0)
    def _get_response(self, classname) -> dict:
        skill_codes = CLASSNAME_TO_SKILL_CODES[classname]

        query = (PlayerSkill.query
                 .filter(PlayerSkill.reference_code.in_(skill_codes))
                 .order_by(PlayerSkill.skill_level.asc()))

        # List contains all skill objects for all skill level - we therefore
        # group them by their reference code
        skill_objects = [skill.to_dict(minimal=True) for skill in query.all()]

        grouped_skills = {
            skill_code: [skill_obj for skill_obj in skill_objects
                         if skill_obj["reference_code"] == skill_code]
            for skill_code in skill_codes
        }

        return {
            "skills": grouped_skills
        }

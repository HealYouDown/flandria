from flask import abort, jsonify, request

from app.api.blueprint import api_bp
from app.models import PlayerSkill, ShipSkill, PlannerBuild, PlannerBuildStar
from flask_jwt_extended import jwt_required, get_current_user
from app.extensions import db

CLASS_TO_SKILLS = {
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


@api_bp.route("/planner/<string:class_>")
def planner(class_: str):
    assert class_ in CLASS_TO_SKILLS.keys(), abort(404)

    if class_ == "ship":
        model = ShipSkill
    else:
        model = PlayerSkill

    skill_codes = CLASS_TO_SKILLS[class_]

    query = (model.query
             .filter(model.skill_code.in_(skill_codes)))

    # returns sorted skill_codes so that the order *never* changes. Otherwise
    # hashes will be get invalid.

    return jsonify({
        "skill_data": [obj.to_dict() for obj in query.all()],
        "skill_codes": sorted(skill_codes),
    }), 200


@api_bp.route("/planner/<string:planner_class>/builds", methods=["GET"])
def get_builds(planner_class: str):
    builds = PlannerBuild.query.filter(PlannerBuild.planner_class == planner_class)
    return jsonify([build.to_dict() for build in builds.all()])


@api_bp.route("/planner/<string:planner_class>/builds", methods=["PUT"])
@jwt_required
def add_build(planner_class: str):
    user = get_current_user()
    json = request.json

    build_name = json.get("build_name")
    build_description = json.get("build_description")[:300]  # first 300 characters only
    selected_level = json.get("selected_level")
    selected_class = json.get("selected_class", None)
    hash_ = json.get("hash")

    build = PlannerBuild(build_name=build_name,
                         build_description=build_description,
                         user_id=user.id,
                         selected_level=selected_level,
                         selected_class=selected_class,
                         planner_class=planner_class,
                         hash=hash_)

    db.session.add(build)
    db.session.commit()

    return jsonify({"msg": "Build was added successfully."}), 201


@api_bp.route("/planner/stars", methods=["PUT"])
@jwt_required
def add_star():
    json = request.json

    build_id = json.get("build_id")
    user_id = json.get("user_id")

    star = PlannerBuildStar(build_id=build_id,
                            user_id=user_id)
    db.session.add(star)
    db.session.commit()

    return jsonify({"msg": "ok"}), 201


@api_bp.route("/planner/stars", methods=["DELETE"])
@jwt_required
def delete_star():
    json = request.json

    build_id = json.get("build_id")
    user_id = json.get("user_id")

    star = (PlannerBuildStar.query
            .filter(PlannerBuildStar.build_id == build_id,
                    PlannerBuildStar.user_id == user_id)
            .first())

    db.session.delete(star)
    db.session.commit()

    return jsonify({"msg": "ok"}), 200
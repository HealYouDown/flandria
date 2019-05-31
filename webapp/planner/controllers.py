from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import current_user, login_required

from webapp import db
from webapp.planner.models import PlayerSkill, ShipSkill, UserBuild, UserBuildStar
from webapp.auth.models import User
from webapp.planner.skills import SKILLS
import operator

planner = Blueprint("planner", __name__, url_prefix="/planner")

@planner.route("/<class_>")
def skillplanner(class_):
    assert class_ in ["explorer", "saint", "noble", "mercenary", "ship"], abort(404)
    skills = SKILLS[class_]

    model = ShipSkill 
    if class_ == "ship":
        model = ShipSkill
    else: model = PlayerSkill

    skill_data = {}
    for obj in db.session.query(model).filter(model.skill_code.in_(skills.keys())).all():
        skill_data[obj.code] = {k: v for k, v in obj.__dict__.items() if not str(k).startswith("_")}

    return render_template("planner/{0}.html".format(class_),
        background="{0}.jpg".format(class_),
        skills=skills, skill_data=skill_data, active_header="planner", title=class_.capitalize()
    )

@planner.route("<class_>/builds") # TODO: Do stars ordering in query
def builds(class_):
    assert class_ in ["explorer", "saint", "noble", "mercenary", "ship"], abort(404)

    builds = db.session.query(UserBuild).filter(UserBuild.class_ == class_, UserBuild.public == True).order_by(UserBuild.stars_count.desc()).all()

    return render_template("planner/builds.html", 
        background="{0}.jpg".format(class_),
        builds=builds, ative_header="planner", title="{0} Builds".format(class_.capitalize()))


@planner.route(("/add_star"), methods=["PUT"])
@login_required
def add_star():
    build_id = request.json["build_id"]

    star = db.session.query(UserBuildStar).filter(UserBuildStar.build_id == build_id, UserBuildStar.user_id == current_user.id).first()

    if star is None: # User has not yet voted on this build
        star = UserBuildStar(user_id=current_user.id, build_id=build_id)
        db.session.add(star)

        build = db.session.query(UserBuild).get(build_id)
        build.stars_count += 1

        db.session.commit()

        return jsonify({"success": True, "build_id": build_id}), 200
    
    return jsonify({"success": False}), 404

@planner.route("/delete_star", methods=["DELETE"])
@login_required
def remove_star():
    build_id = request.json["build_id"]

    star = db.session.query(UserBuildStar).filter(UserBuildStar.build_id == build_id, UserBuildStar.user_id == current_user.id).first()
    if star is None:
        return jsonify({"success": False}), 404

    db.session.delete(star)

    build = db.session.query(UserBuild).get(build_id)
    build.stars_count -= 1

    db.session.commit()

    return jsonify({"success": True, "build_id": build_id}), 200

@planner.route("/add_build", methods=["PUT"])
@login_required
def add_build():
    content = request.json

    try:
        build = UserBuild(
            user_id=current_user.id, 
            class_=content["class"], 
            public=content["public"], 
            description=content["description"], 
            title=content["title"], 
            hash=content["hash"],
            selected_level=content["selected_level"],
            selected_class=content["selected_class"],
        )
        db.session.add(build)
        db.session.commit()
    except Exception as e:
        return jsonify({"success": False, "error": e}), 500

    return jsonify({"success": True}), 200

@planner.route("/delete_build", methods=["DELETE"])
@login_required
def delete_build():
    build_id = request.json["build_id"]

    build = db.session.query(UserBuild).get(build_id)

    if current_user.id == build.user_id:
        db.session.delete(build)
        db.session.commit()
    else:
        return jsonify({"success": False, "error": "Not your build"}), 403

    return jsonify({"success": True, "build_id": build_id}), 200

"""
@planner.route("/create_image", methods=["GET", "POST"])
def create_image(): # TODO
    data = request.json

    return jsonify({"success": False})
"""

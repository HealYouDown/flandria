from flask_restful import Resource
from flask import abort, request
from app.planner.models import PlayerSkill, ShipSkill, UserBuild, UserBuildStar
from app.extensions import db
from flask_praetorian import auth_required, current_user
from app.decorators import auth_optional


class PlannerData(Resource):
    noble_skills = [
        "cp002300", "ck500000", "cp008700", "cp006800", "cp010200", "cp002400",
        "cp006200", "cp008300", "cp006000", "cp002600", "cp006100", "cp008200",
        "cp002900", "cp006400", "cp002500", "cp006300", "cp008800", "cp008900",
        "cp006700", "cp002800", "cp006600", "cp009100", "cp007000", "cp002700",
        "cp003000", "cp006500", "cp006900", "cp008400", "cp008600", "cp008500"
    ]

    explorer_skills = [
        "ck500000", "ck000700", "ck005200", "ck008700", "ck009000", "ck005800",
        "ck009100", "ck005300", "ck008500", "ck000800", "ck001000", "ck000900",
        "ck008400", "ck008800", "ck005900", "ck005400", "ck001100", "ck001200",
        "ck009200", "ck008000", "ck008300", "ck007900", "ck001500", "ck001300",
        "ck005700", "ck005500", "ck008100", "ck005600", "ck008600"
    ]

    mercenary_skills = [
        "ck500000", "ck004600", "ck000400", "ck008900", "ck000100", "ck004700",
        "ck004200", "ck004400", "ck007000", "ck003900", "ck000000", "ck004000",
        "ck004300", "ck004500", "ck007600", "ck007400", "ck004100", "ck004800",
        "ck000500", "ck007100", "ck004900", "ck005100", "ck000300", "ck005000",
        "ck007500", "ck007800", "ck000200", "ck000600", "ck007700", "ck007200"
    ]

    saint_skills = [
        "cp003500", "cp007700", "cp007600", "cp009600", "cp003100", "cp008000",
        "cp003200", "cp007100", "cp009300", "cp009200", "cp007800", "cp003800",
        "cp003400", "cp003600", "cp009400", "cp007200", "cp007900", "cp003300",
        "cp009500", "cp003700", "cp007300", "cp007400", "cp009800", "cp009700",
        "cp010100", "ck500000", "cp010300", "cp008100", "cp007500", "cp009900"
    ]

    ship_skills = [
        "sksinso00", "skpogye00", "skjojun00", "skwehyu00", "skpokba00", "skchain00",
        "skadomi00", "skhwaks00", "skstst000", "skgwant00", "skrange00", "skunpro00",
        "skgyeon00", "skjilju00", "skwinds00", "skpagoe00", "skransh00", "skadest00",
        "skyeonb00", "skgeunj00", "skangae00", "skhide000", "skdarks00", "skchung00",
        "skload000", "skflash00", "skavoid00", "skjaesa00", "skhambo00", "sksiles00",
        "skchiyu00", "skshipr00", "skchund00", "skendur00", "sksick000", "skspecs00",
        "skturn000", "skyuck000", "skjunja00", "skgyeol00", "skjunso00", "skshotm00",
        "skdouca00", "sklimit00",
    ]

    def get(self, class_):
        assert class_ in ["noble", "saint", "explorer",
                          "mercenary", "ship"], abort(404, "Class not found.")

        if class_ == "noble":
            skill_codes = self.noble_skills
            model = PlayerSkill
        elif class_ == "explorer":
            skill_codes = self.explorer_skills
            model = PlayerSkill
        elif class_ == "saint":
            skill_codes = self.saint_skills
            model = PlayerSkill
        elif class_ == "mercenary":
            skill_codes = self.mercenary_skills
            model = PlayerSkill
        elif class_ == "ship":
            skill_codes = self.ship_skills
            model = ShipSkill

        skills = {
            s.code: s.to_dict() for s in db.session.query(model)
            .filter(model.skill_code.in_(skill_codes))
            .all()
        }

        return skills, 200


class PlannerBuild(Resource):
    @auth_optional
    def get(self, class_, build_id=None, user=None):
        includes = [
            "description", "index", "selected_class", "selected_level", "stars.build_id",
            "stars.user_id", "time", "title", "stars_count", "user.id", "user.username",
            "hash", "class_",
        ]

        query = db.session.query(UserBuild)\
            .filter(UserBuild.class_ == class_, UserBuild.public)

        # User is logged in and parameter ?allUserBuilds=1 is given
        # returns all builds for that user
        if user is not None and bool(int(request.args.get("allUserBuilds", 0))) and class_ == "all":
            query = db.session.query(UserBuild)\
                .filter(UserBuild.user_id == user.id)

        return [b.to_dict(includes=includes) for b in query.all()]

    @auth_required
    def put(self, class_, build_id=None):
        data = request.json
        user = current_user()

        if not data:
            return abort(400, "Data missing")

        title = data.get("title", None)
        public = data.get("public", False)
        description = data.get("description", None)
        hash_ = data.get("hash", None)
        selected_level = data.get("selected_level", None)
        selected_class = data.get("selected_class", None)

        build = UserBuild(
            user_id=user.id,
            title=title,
            description=description,
            public=public,
            class_=class_,
            hash=hash_,
            selected_class=selected_class,
            selected_level=selected_level,
        )
        db.session.add(build)
        db.session.commit()

        return {"message": "Build was added successfully"}, 201

    @auth_required
    def delete(self, class_, build_id):
        user = current_user()

        build = UserBuild.query.get(build_id)
        if build.user_id != user.id:
            return abort(403, "Not your build!")

        db.session.delete(build)
        db.session.commit()

        return {"message": "Build was deleted successfully"}, 200


class PlannerBuildStar(Resource):
    @auth_required
    def put(self, class_, build_id):
        user = current_user()

        star = UserBuildStar(user_id=user.id, build_id=build_id)
        db.session.add(star)
        db.session.commit()

        return {"message": "Star was added successfully."}, 201

    @auth_required
    def delete(self, class_, build_id):
        user = current_user()

        star = db.session.query(UserBuildStar)\
            .filter(UserBuildStar.user_id == user.id, UserBuildStar.build_id == build_id)\
            .first()

        if star is None:
            return abort(401, "Object was not found")

        db.session.delete(star)
        db.session.commit()

        return {"message": "Star was deleted successfully."}, 200


def register_planner_endpoints(api):
    api.add_resource(PlannerData, "/planner/<class_>")
    api.add_resource(
        PlannerBuild,
        "/planner/<class_>/builds",
        "/planner/<class_>/builds/<build_id>",
    )
    api.add_resource(PlannerBuildStar, "/planner/<class_>/builds/<build_id>/stars")

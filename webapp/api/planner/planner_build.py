from flask import request
from flask_jwt_extended import jwt_required, current_user
from webapp.models.tables.planner_build import PlannerStar, PlannerBuild
from flask_restx import Resource, abort
from webapp.extensions import db
from webapp.models.enums import CharacterClass
from sqlalchemy import func


class PlannerBuildView(Resource):
    def get(self, classname: str):
        try:
            base_class = getattr(CharacterClass, classname)
        except AttributeError:
            abort(404)

        query = db.session.query(
            PlannerBuild,
            func.count(PlannerStar.user_id).label("stars_count")
        ).join(
            PlannerStar,
        ).group_by(
            "stars_count DESC"
        )

        if base_class == CharacterClass.noble:
            classes = [CharacterClass.noble,
                       CharacterClass.court_magician,
                       CharacterClass.magic_knight]
        elif base_class == CharacterClass.explorer:
            classes = [CharacterClass.explorer,
                       CharacterClass.sniper,
                       CharacterClass.excavator]
        elif base_class == CharacterClass.saint:
            classes = [CharacterClass.saint,
                       CharacterClass.shaman,
                       CharacterClass.priest]
        elif base_class == CharacterClass.mercenary:
            classes = [CharacterClass.mercenary,
                       CharacterClass.gladiator,
                       CharacterClass.guardian_swordsman]
        else:
            classes = []

        if classes:
            query = query.filter(PlannerBuild.character_class.in_(classes))

        return [
            build.to_dict() for build in query.all()
        ]

    @jwt_required
    def post(self):
        # Check if user already has more than 20 builds
        user_builds_count = PlannerBuild.query.filter(
            PlannerBuild.user_id == current_user.id).count()

        if user_builds_count > 10:
            return {
                "message": "Too many builds."
            }, 401

        json = request.json

        needed_keys = ["title", "description", "hash", "character_class"]

        if not all(key in json for key in needed_keys):
            abort(400)

        # Check title length > 2, < 100
        if not (2 < len(json["title"].strip()) < 100):
            abort(400)

        try:
            char_class = CharacterClass(json["character_class"])
        except ValueError:
            abort(400)

        build = PlannerBuild(
            user_id=current_user.id,
            build_hash=json["hash"],
            build_title=json["title"],
            build_description=json["description"],
            character_class=char_class,
        )
        db.session.add(build)
        db.session.commit()

        return {}, 201


    @jwt_required
    def delete(self, id: int):
        build = PlannerBuild.query.get_or_404(id)

        if build.user_id != current_user.id:
            abort(401)

        db.session.delete(build)
        db.session.commit()

        return {}, 204


class PlannerStarView(Resource):
    @jwt_required
    def post(self, build_id: int):
        # Check if already voted on that build
        star = PlannerStar.query.filter(
            PlannerStar.user_id == current_user.id,
            build_id == build_id,
        ).first()

        if star:
            abort(401)

        db.session.add(PlannerStar(
            build_id=build_id,
            user_id=current_user.id,
        ))
        db.session.commit()

    @jwt_required
    def delete(self, build_id: int):
        PlannerStar.query.filter(
            PlannerStar.user_id == current_user.id,
            build_id == build_id,
        ).delete()
        db.session.commit()

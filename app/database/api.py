from flask import abort, request
from flask_praetorian import roles_accepted, current_user
from flask_restful import Resource

import app.database.models as db_models
import app.database.utils as db_utils
from app.decorators import auth_optional
from app.extensions import db
from app.utils import tablename_to_class_name

from app.webhooks import send_add_drop_webhook, send_delete_drop_webhook, send_edit_drop_webhook


class Database(Resource):
    def get(self, table=None, code=None):
        if table is not None and code is None:
            return self._table_overview(table)

        elif table is not None and code is not None:
            return self._detailed_overview(table, code)

    @auth_optional
    def _table_overview(self, table, user=None):
        assert table in db_utils.tables.keys(), abort(404, "Table was not found.")

        table_cls_name = tablename_to_class_name(table)
        table_cls = getattr(db_models, table_cls_name)

        query = db.session.query(table_cls)\
            .filter(table_cls.code.notin_(db_utils.get_excluded_codes()))

        if user is None or not user.can_see_hidden:
            query = query.filter(table_cls.code.notin_(
                db_utils.get_hidden_codes(user=None)))

        items = [item.to_dict(overview=True) for item in query.all()]
        return items, 200

    @auth_optional
    def _detailed_overview(self, table, code, user=None):
        table_data = db_utils.tables.get(table, None)
        if table_data is None:
            return abort(404, "Table was not found.")

        table_cls_name = tablename_to_class_name(table)
        table_cls = getattr(db_models, table_cls_name)

        query = db.session.query(table_cls)\
            .filter(table_cls.code == code,
                    table_cls.code.notin_(db_utils.get_excluded_codes())
                    )

        if user is None or not user.can_see_hidden:
            query = query.filter(table_cls.code.notin_(
                db_utils.get_hidden_codes(user=None)))

        item = query.first()
        if item is None:
            return abort(404, "Item was not found.")

        item_dict = item.to_dict()
        for key in table_data:
            if key == "upgrade_data":
                item_dict["upgrade_data"] = db_utils.get_upgrade_data(item_dict["upgrade_code"])
            else:
                func = getattr(db_utils, f"get_{key}")
                item_dict[key] = func(item_dict["code"])

        return item_dict, 200


class Search(Resource):
    @auth_optional
    def get(self, user=None):
        search_string = request.args.get("s", "")

        if not search_string:
            return [], 200

        matching_items = db_utils.search_itemlist(
            string=search_string,
            user=user,
        )

        return matching_items, 200


class Drop(Resource):
    @roles_accepted("can_edit_drops")
    def patch(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        item_code = data.get("item_code", None)
        monster_code = data.get("monster_code", None)
        quantity = data.get("quantity", None)

        if item_code is None:
            return abort(400, "Item code is missing")

        if monster_code is None:
            return abort(400, "Monster code is missing.")

        if quantity is None:
            return abort(400, "Item quantity is missing.")

        drop = db_models.Drop.query\
            .filter(db_models.Drop.monster_code == monster_code,
                    db_models.Drop.item_code == item_code)\
            .first()

        if drop is None:
            return abort(409, "Drop does not exist.")

        # webhook
        monster = db_models.Monster.query.get(monster_code)
        item = db_models.ItemList.query.get(item_code)
        user = current_user()

        send_edit_drop_webhook(monster, item, quantity, user)

        drop.quantity = quantity
        db.session.commit()

        return {"message": "Drop was updated successfully."}, 201

    @roles_accepted("can_edit_drops")
    def put(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        item_code = data.get("item_code", None)
        monster_code = data.get("monster_code", None)
        quantity = data.get("quantity", 1)

        if item_code is None:
            return abort(400, "Item code is missing")

        if monster_code is None:
            return abort(400, "Monster code is missing.")

        drop = db_models.Drop.query\
            .filter(db_models.Drop.monster_code == monster_code,
                    db_models.Drop.item_code == item_code)\
            .first()

        if drop is not None:
            return abort(409, "Drop already exists.")

        # Sending a webhook
        monster = db_models.Monster.query.get(monster_code)
        item = db_models.ItemList.query.get(item_code)
        user = current_user()

        send_add_drop_webhook(monster, item, user)

        # Actually adding drop to database
        drop = db_models.Drop(monster_code=monster_code, item_code=item_code, quantity=quantity)
        db.session.add(drop)
        db.session.commit()

        return {"message": "Drop was added successfully."}, 201

    @roles_accepted("can_edit_drops")
    def delete(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        item_code = data.get("item_code", None)
        monster_code = data.get("monster_code", None)

        if item_code is None:
            return abort(400, "Item code is missing")

        if monster_code is None:
            return abort(400, "Monster code is missing.")

        drop = db_models.Drop.query\
            .filter(db_models.Drop.monster_code == monster_code,
                    db_models.Drop.item_code == item_code)\
            .first()

        if drop is None:
            return abort(404, "Drop was not found.")

        # Sending a webhook
        monster = db_models.Monster.query.get(monster_code)
        item = db_models.ItemList.query.get(item_code)
        user = current_user()

        send_delete_drop_webhook(monster, item, user)

        # Actually deleting drop
        db.session.delete(drop)
        db.session.commit()

        return {"message": "Drop was deleted successfully."}, 200


class HiddenItem(Resource):
    @roles_accepted("admin")
    def get(self):
        return db_utils.get_hidden_codes(return_always=True, user=None)

    @roles_accepted("admin")
    def put(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        code = data.get("code", None)

        if code is None:
            return abort(400, "Item code is missing.")

        item = db.session.query(db_models.HiddenItem).filter(db_models.HiddenItem.code == code).first()

        if item is not None:
            return abort(422, "Item code already exists.")

        item = db_models.HiddenItem(code=code)
        db.session.add(item)
        db.session.commit()

        return {"message": "Hidden item was added successfully."}, 201

    @roles_accepted("admin")
    def delete(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        code = data.get("code", None)

        if code is None:
            return abort(400, "Item code is missing.")

        item = db.session.query(db_models.HiddenItem).filter(db_models.HiddenItem.code == code).first()

        if item is None:
            return abort(422, "Item was already deleted.")

        db.session.delete(item)
        db.session.commit()

        return {"message": "Hidden item was deleted successfully."}, 200


class ExcludedItem(Resource):
    @roles_accepted("admin")
    def get(self):
        return db_utils.get_excluded_codes(return_always=True, user=None)

    @roles_accepted("admin")
    def put(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        code = data.get("code", None)

        if code is None:
            return abort(400, "Item code is missing.")

        item = db.session.query(db_models.ExcludedItem).filter(db_models.ExcludedItem.code == code).first()

        if item is not None:
            return abort(422, "Item code already exists.")

        item = db_models.ExcludedItem(code=code)
        db.session.add(item)
        db.session.commit()

        return {"message": "Excluded item was added successfully."}, 201

    @roles_accepted("admin")
    def delete(self):
        data = request.json
        if data is None:
            return abort(400, "Json data is missing.")

        code = data.get("code", None)

        if code is None:
            return abort(400, "Item code is missing.")

        item = db.session.query(db_models.ExcludedItem).filter(db_models.ExcludedItem.code == code).first()

        if item is None:
            return abort(422, "item was already deleted.")

        db.session.delete(item)
        db.session.commit()

        return {"message": "Excluded item was deleted successfully."}, 200


def register_database_endpoints(api):
    # Database Table Overview and Detailed Page view
    api.add_resource(
        Database,
        "/database/<string:table>",
        "/database/<string:table>/<string:code>"
    )

    # Search
    api.add_resource(Search, "/search", endpoint="search_database")

    # Drops
    api.add_resource(Drop, "/drops", endpoint="drops")

    # Hidden Items
    api.add_resource(HiddenItem, "/hidden_items", endpoint="hidden_items")

    # Excluded Items
    api.add_resource(ExcludedItem, "/excluded_items", endpoint="excluded_items")

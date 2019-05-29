from flask import Blueprint, render_template, request, jsonify
from webapp.database.models import ExcludeFromView
from webapp import db
from flask_login import login_required
from webapp.decorators import admin_required

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard.route("/excludes")
@login_required
@admin_required
def excludes():
    excludes = ExcludeFromView.query.all()
    return render_template("dashboard/excludes.html", excludes=excludes)

@dashboard.route("/excludes/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_exclude():
    data = request.json

    db.session.query(ExcludeFromView).filter(ExcludeFromView.item_code == data["item_code"]).delete()
    db.session.commit()

    return jsonify({"success": True}), 200
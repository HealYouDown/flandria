from webapp.models import User


def user_lookup_loader(_jwt_header, jwt_data):
    identity = jwt_data["identity"]
    return User.query.filter(User.id == identity["id"]).one_or_none()

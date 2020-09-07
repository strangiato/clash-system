from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from clash_api.extensions import apispec
from clash_api.api.resources import UserResource, UserList
from clash_api.api.schemas import UserSchema
from clash_api.api.resources import ClanResource, ClanList
from clash_api.api.schemas import ClanSchema

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(UserResource, "/clans/<int:clan_id>", endpoint="clan_by_id")
api.add_resource(UserList, "/clans", endpoint="clans")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)

    apispec.spec.components.schema("ClanSchema", schema=ClanSchema)
    apispec.spec.path(view=ClanResource, app=current_app)
    apispec.spec.path(view=ClanList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints,
    returning correct JSON response with associated HTTP 400 Status
    (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

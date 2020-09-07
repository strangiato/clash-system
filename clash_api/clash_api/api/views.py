from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from clash_api.extensions import apispec
from clash_api.api.resources import UserResource, UserList
from clash_api.api.schemas import UserSchema
from clash_api.api.resources import ClanResource, ClanList
from clash_api.api.schemas import ClanSchema
from clash_api.api.resources import PlayerResource, PlayerList
from clash_api.api.schemas import PlayerSchema

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(ClanResource, "/clans/<int:clan_id>", endpoint="clan_by_id")
api.add_resource(ClanList, "/clans", endpoint="clans")

api.add_resource(PlayerResource, "/players/<int:player_id>", endpoint="player_by_id")
api.add_resource(PlayerList, "/players", endpoint="players")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)

    apispec.spec.components.schema("ClanSchema", schema=ClanSchema)
    apispec.spec.path(view=ClanResource, app=current_app)
    apispec.spec.path(view=ClanList, app=current_app)

    apispec.spec.components.schema("PlayerSchema", schema=PlayerSchema)
    apispec.spec.path(view=PlayerResource, app=current_app)
    apispec.spec.path(view=PlayerList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints,
    returning correct JSON response with associated HTTP 400 Status
    (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400

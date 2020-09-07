from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from clash_api.api.schemas import PlayerSchema
from clash_api.models import Player
from clash_api.extensions import db
from clash_api.commons.pagination import paginate


class PlayerResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: Player_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  player: PlayerSchema
        404:
          description: player does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: player_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              PlayerSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: player updated
                  player: PlayerSchema
        404:
          description: player does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: player_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: player deleted
        404:
          description: player does not exists
    """

    method_decorators = [jwt_required]

    def get(self, player_id):
        schema = PlayerSchema()
        player = Player.query.get_or_404(player_id)
        return {"player": schema.dump(player)}

    def put(self, player_id):
        schema = PlayerSchema(partial=True)
        player = Player.query.get_or_404(player_id)
        player = schema.load(request.json, instance=player)

        db.session.commit()

        return {"msg": "player updated", "player": schema.dump(player)}

    def delete(self, player_id):
        player = Player.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()

        return {"msg": "player deleted"}


class PlayerList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/PlayerSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              PlayerSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: player created
                  player: PlayerSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = PlayerSchema(many=True)
        query = Player.query
        return paginate(query, schema)

    def post(self):
        schema = PlayerSchema()
        player = schema.load(request.json)

        db.session.add(player)
        db.session.commit()

        return {"msg": "player created", "player": schema.dump(player)}, 201

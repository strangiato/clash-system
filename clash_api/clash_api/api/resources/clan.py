from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from clash_api.api.schemas import ClanSchema
from clash_api.models import Clan
from clash_api.extensions import db
from clash_api.commons.pagination import paginate


class ClanResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: Clan_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  clan: ClanSchema
        404:
          description: clan does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: clan_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              ClanSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: clan updated
                  clan: ClanSchema
        404:
          description: clan does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: clan_id
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
                    example: clan deleted
        404:
          description: clan does not exists
    """

    method_decorators = [jwt_required]

    def get(self, clan_id):
        schema = ClanSchema()
        clan = Clan.query.get_or_404(clan_id)
        return {"clan": schema.dump(clan)}

    def put(self, clan_id):
        schema = ClanSchema(partial=True)
        clan = Clan.query.get_or_404(clan_id)
        clan = schema.load(request.json, instance=clan)

        db.session.commit()

        return {"msg": "clan updated", "clan": schema.dump(clan)}

    def delete(self, clan_id):
        clan = Clan.query.get_or_404(clan_id)
        db.session.delete(clan)
        db.session.commit()

        return {"msg": "clan deleted"}


class ClanList(Resource):
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
                          $ref: '#/components/schemas/ClanSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              ClanSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: clan created
                  clan: ClanSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = ClanSchema(many=True)
        query = Clan.query
        return paginate(query, schema)

    def post(self):
        schema = ClanSchema()
        clan = schema.load(request.json)

        db.session.add(clan)
        db.session.commit()

        return {"msg": "clan created", "clan": schema.dump(clan)}, 201

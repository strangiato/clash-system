from clash_api.models import Player
from clash_api.extensions import ma, db


class PlayerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Player
        sqla_session = db.session
        load_instance = True

from clash_api.models import Clan
from clash_api.extensions import ma, db


class ClanSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Clan
        sqla_session = db.session
        load_instance = True

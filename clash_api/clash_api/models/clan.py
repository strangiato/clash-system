from clash_api.extensions import db


class Clan(db.Model):
    """Clan model"""

    id = db.Column(db.Integer, primary_key=True)
    # member = db.relationship("Player")
    clanname = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    required_trophies = db.Column(db.Integer, nullable=False)
    clan_score = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        super(Clan, self).__init__(**kwargs)

    def __repr__(self):
        return "<Clan %s>" % self.clanname

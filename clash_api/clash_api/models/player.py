from clash_api.extensions import db


class Player(db.Model):
    """Player model"""

    id = db.Column(db.Integer, primary_key=True)
    # clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'))
    name = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.String(80), unique=True, nullable=False)
    trophies = db.Column(db.Integer, unique=False, nullable=True)
    best_trophies = db.Column(db.Integer, unique=False, nullable=True)
    donations = db.Column(db.Integer, nullable=False)
    donations_received = db.Column(db.Integer, nullable=False)
    battle_count = db.Column(db.Integer, unique=False, nullable=True)
    three_crown_wins = db.Column(db.Integer, unique=False, nullable=True)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

    def __repr__(self):
        return "<Player %s>" % self.name

import factory
from clash_api.models import User, Clan, Player


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


class ClanFactory(factory.Factory):

    clanname = factory.Sequence(lambda n: "clan%d" % n)
    tag = factory.Sequence(lambda n: "#%d" % n)

    description = factory.Faker("sentence")
    required_trophies = factory.Faker("random_int")
    clan_score = factory.Faker("random_int")

    class Meta:
        model = Clan


class PlayerFactory(factory.Factory):

    # clan = factory.SubFactory(ClanFactory)

    name = factory.Faker("first_name")
    tag = factory.Sequence(lambda n: "#%d" % n)

    trophies = factory.Faker("random_int")
    best_trophies = factory.Faker("random_int")
    donations = factory.Faker("random_int")
    donations_received = factory.Faker("random_int")
    battle_count = factory.Faker("random_int")
    three_crown_wins = factory.Faker("random_int")

    class Meta:
        model = Player

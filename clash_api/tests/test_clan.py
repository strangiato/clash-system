from flask import url_for
from clash_api.models import Clan


def test_get_clan(client, db, clan, admin_headers):
    # test 404
    clan_url = url_for("api.clan_by_id", clan_id="100000")
    rep = client.get(clan_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(clan)
    db.session.commit()

    # test get_clan
    clan_url = url_for("api.clan_by_id", clan_id=clan.id)
    rep = client.get(clan_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["clan"]
    assert data["clanname"] == clan.clanname
    assert data["tag"] == clan.tag
    assert data["description"] == clan.description
    assert data["required_trophies"] == clan.required_trophies
    assert data["clan_score"] == clan.clan_score


def test_put_clan(client, db, clan, admin_headers):
    # test 404
    clan_url = url_for("api.clan_by_id", clan_id="100000")
    rep = client.put(clan_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(clan)
    db.session.commit()

    data = {"clanname": "updated"}

    clan_url = url_for("api.clan_by_id", clan_id=clan.id)
    # test update clan
    rep = client.put(clan_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["clan"]
    assert data["clanname"] == "updated"
    assert data["tag"] == clan.tag
    assert data["description"] == clan.description
    assert data["required_trophies"] == clan.required_trophies
    assert data["clan_score"] == clan.clan_score


def test_delete_clan(client, db, clan, admin_headers):
    # test 404
    clan_url = url_for("api.clan_by_id", clan_id="100000")
    rep = client.delete(clan_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(clan)
    db.session.commit()

    # test get_clan

    clan_url = url_for("api.clan_by_id", clan_id=clan.id)
    rep = client.delete(clan_url, headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Clan).filter_by(id=clan.id).first() is None


def test_create_clan(client, db, admin_headers):
    # test bad data
    clans_url = url_for("api.clans")
    data = {"clanname": "created"}
    rep = client.post(clans_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["tag"] = "create@mail.com"
    data["description"] = "This is a clan description"
    data["required_trophies"] = 3500
    data["clan_score"] = 4321

    rep = client.post(clans_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    clan = db.session.query(Clan).filter_by(id=data["clan"]["id"]).first()

    assert clan.clanname == "created"
    assert clan.tag == "create@mail.com"
    assert clan.description == "This is a clan description"
    assert clan.required_trophies == 3500
    assert clan.clan_score == 4321


def test_get_all_clan(client, db, clan_factory, admin_headers):
    clans_url = url_for("api.clans")
    clans = clan_factory.create_batch(30)

    db.session.add_all(clans)
    db.session.commit()

    rep = client.get(clans_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for clan in clans:
        assert any(u["id"] == clan.id for u in results["results"])

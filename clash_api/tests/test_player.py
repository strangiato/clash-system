from flask import url_for
from clash_api.models import Player


def test_get_player(client, db, player, admin_headers):
    # test 404
    player_url = url_for("api.player_by_id", player_id="100000")
    rep = client.get(player_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(player)
    db.session.commit()

    # test get_player
    player_url = url_for("api.player_by_id", player_id=player.id)
    rep = client.get(player_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["player"]
    assert data["name"] == player.name
    assert data["tag"] == player.tag
    assert data["trophies"] == player.trophies
    assert data["best_trophies"] == player.best_trophies
    assert data["donations"] == player.donations
    assert data["donations_received"] == player.donations_received
    assert data["battle_count"] == player.battle_count
    assert data["three_crown_wins"] == player.three_crown_wins


def test_put_player(client, db, player, admin_headers):
    # test 404
    player_url = url_for("api.player_by_id", player_id="100000")
    rep = client.put(player_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(player)
    db.session.commit()

    data = {"name": "updated"}

    player_url = url_for("api.player_by_id", player_id=player.id)
    # test update player
    rep = client.put(player_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["player"]

    # print(data)
    assert data["name"] == "updated"
    assert data["tag"] == player.tag
    assert data["trophies"] == player.trophies
    assert data["best_trophies"] == player.best_trophies
    assert data["donations"] == player.donations
    assert data["donations_received"] == player.donations_received
    assert data["battle_count"] == player.battle_count
    assert data["three_crown_wins"] == player.three_crown_wins


def test_delete_player(client, db, player, admin_headers):
    # test 404
    player_url = url_for("api.player_by_id", player_id="100000")
    rep = client.delete(player_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(player)
    db.session.commit()

    # test get_player

    player_url = url_for("api.player_by_id", player_id=player.id)
    rep = client.delete(player_url, headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Player).filter_by(id=player.id).first() is None


def test_create_player(client, db, admin_headers):
    # test bad data
    players_url = url_for("api.players")
    data = {"name": "created"}
    rep = client.post(players_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["tag"] = "create@mail.com"
    data["trophies"] = 3215
    data["best_trophies"] = 3500
    data["donations"] = 134
    data["donations_received"] = 321
    data["battle_count"] = 4321
    data["three_crown_wins"] = 1234

    rep = client.post(players_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    player = db.session.query(Player).filter_by(id=data["player"]["id"]).first()

    assert player.name == "created"
    assert player.tag == "create@mail.com"
    assert player.trophies == 3215
    assert player.best_trophies == 3500
    assert player.donations == 134
    assert player.donations_received == 321
    assert player.battle_count == 4321
    assert player.three_crown_wins == 1234


def test_get_all_player(client, db, player_factory, admin_headers):
    players_url = url_for("api.players")
    players = player_factory.create_batch(30)

    db.session.add_all(players)
    db.session.commit()

    rep = client.get(players_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for player in players:
        assert any(u["id"] == player.id for u in results["results"])

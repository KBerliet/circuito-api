from tests.test_drivers import create_driver
from tests.test_races import create_race
from tests.test_teams import create_team


def setup_driver_and_race(client):
    # helper que monta o cenario completo: equipe -> piloto + corrida
    team = create_team(client).json()
    driver = create_driver(client, team["id"]).json()
    race = create_race(client).json()
    return driver, race


def create_result(client, driver_id, race_id, position=1, points=25.0):
    return client.post(
        "/results",
        json={
            "position": position,
            "points": points,
            "driver_id": driver_id,
            "race_id": race_id,
        },
    )


def test_create_result_success(client):
    driver, race = setup_driver_and_race(client)
    response = create_result(client, driver["id"], race["id"])
    assert response.status_code == 201
    data = response.json()
    assert data["position"] == 1
    assert data["driver_id"] == driver["id"]


def test_create_result_invalid_driver_fails(client):
    _, race = setup_driver_and_race(client)
    response = create_result(client, driver_id=9999, race_id=race["id"])
    assert response.status_code == 400


def test_create_result_invalid_race_fails(client):
    driver, _ = setup_driver_and_race(client)
    response = create_result(client, driver_id=driver["id"], race_id=9999)
    assert response.status_code == 400


def test_create_result_missing_field_fails(client):
    response = client.post("/results", json={"position": 1})
    assert response.status_code == 422


def test_list_results_empty(client):
    response = client.get("/results")
    assert response.status_code == 200
    assert response.json() == []


def test_list_results_after_create(client):
    driver, race = setup_driver_and_race(client)
    create_result(client, driver["id"], race["id"])
    response = client.get("/results")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_results_by_race_success(client):
    driver, race = setup_driver_and_race(client)
    create_result(client, driver["id"], race["id"])
    response = client.get(f"/results/race/{race['id']}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_results_by_race_not_found(client):
    response = client.get("/results/race/9999")
    assert response.status_code == 404
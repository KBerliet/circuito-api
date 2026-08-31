from tests.test_teams import create_team


def create_driver(client, team_id, name="Max Verstappen", number=1, nationality="Dutch"):
    return client.post(
        "/drivers",
        json={
            "name": name,
            "number": number,
            "nationality": nationality,
            "team_id": team_id,
        },
    )


def test_create_driver_success(client):
    team = create_team(client).json()
    response = create_driver(client, team["id"])
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Max Verstappen"
    assert data["team_id"] == team["id"]


def test_create_driver_invalid_team_fails(client):
    response = create_driver(client, team_id=9999)
    assert response.status_code == 400


def test_create_driver_missing_field_fails(client):
    response = client.post("/drivers", json={"name": "Max Verstappen"})
    assert response.status_code == 422


def test_create_driver_invalid_number_fails(client):
    team = create_team(client).json()
    response = create_driver(client, team["id"], number=0)  # number tem que ser > 0
    assert response.status_code == 422


def test_list_drivers_empty(client):
    response = client.get("/drivers")
    assert response.status_code == 200
    assert response.json() == []


def test_list_drivers_after_create(client):
    team = create_team(client).json()
    create_driver(client, team["id"])
    response = client.get("/drivers")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_driver_by_id_success(client):
    team = create_team(client).json()
    driver = create_driver(client, team["id"]).json()
    response = client.get(f"/drivers/{driver['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Max Verstappen"


def test_get_driver_by_id_not_found(client):
    response = client.get("/drivers/9999")
    assert response.status_code == 404

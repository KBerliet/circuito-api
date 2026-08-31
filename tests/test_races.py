def create_race(
    client,
    name="Grande Prêmio de São Paulo",
    circuit="Interlagos",
    country="Brasil",
    season=2026,
):
    return client.post(
        "/races",
        json={"name": name, "circuit": circuit, "country": country, "season": season},
    )


def test_create_race_success(client):
    response = create_race(client)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Grande Prêmio de São Paulo"
    assert "id" in data


def test_create_race_missing_field_fails(client):
    response = client.post("/races", json={"name": "Grande Prêmio de São Paulo"})  # falta o resto
    assert response.status_code == 422


def test_create_race_invalid_season_fails(client):
    response = create_race(client, season=1800)  # antes da f1 existir (regra do schema: > 1950)
    assert response.status_code == 422


def test_list_races_empty(client):
    response = client.get("/races")
    assert response.status_code == 200
    assert response.json() == []


def test_get_race_by_id_success(client):
    race = create_race(client).json()
    response = client.get(f"/races/{race['id']}")
    assert response.status_code == 200
    assert response.json()["circuit"] == "Interlagos"


def test_get_race_by_id_not_found(client):
    response = client.get("/races/9999")
    assert response.status_code == 404

def create_team(client, name="Red Bull Racing", nationality="Austrian", base="Milton Keynes"):
    # funcao auxiliar pra nao repetir esse bloco em todo teste que precisa de uma equipe
    return client.post(
        "/teams",
        json={"name": name, "nationality": nationality, "base": base},
    )


def test_create_team_success(client):
    response = create_team(client)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Red Bull Racing"
    assert "id" in data


def test_create_team_duplicate_name_fails(client):
    create_team(client)
    response = create_team(client)  # cria de novo com o mesmo nome
    assert response.status_code == 400


def test_create_team_missing_field_fails(client):
    response = client.post("/teams", json={"name": "Ferrari"})  # falta nationality
    assert response.status_code == 422


def test_list_teams_empty(client):
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []


def test_list_teams_after_create(client):
    create_team(client)
    response = client.get("/teams")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_team_by_id_success(client):
    created = create_team(client).json()
    response = client.get(f"/teams/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Red Bull Racing"


def test_get_team_by_id_not_found(client):
    response = client.get("/teams/9999")
    assert response.status_code == 404

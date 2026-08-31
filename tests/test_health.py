def test_health_check_status_code(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_body(client):
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_check_wrong_method_not_allowed(client):
    response = client.post("/health")
    assert response.status_code == 405
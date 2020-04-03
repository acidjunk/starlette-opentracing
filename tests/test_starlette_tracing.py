def test_view_ok(client):
    response = client.get("/foo/")
    assert response.status_code == 200

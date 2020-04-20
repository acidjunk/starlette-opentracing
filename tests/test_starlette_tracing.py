def test_view_ok(client):
    """Test loading a starlette app with the trace enabled and query a view."""
    response = client.get("/foo/")
    assert response.status_code == 200

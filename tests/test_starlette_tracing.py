
def test_view_ok(client):
    # Do a request
    response = client.get("/foo/")


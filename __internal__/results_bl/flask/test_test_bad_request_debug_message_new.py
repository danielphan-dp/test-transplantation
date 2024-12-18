import pytest
from flask import Flask, request

@pytest.mark.parametrize('debug', (True, False))
def test_post_method(app, client, debug):
    app.config["DEBUG"] = debug

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data=None, content_type="application/json")
    assert rv.status_code == 200
    assert rv.data == b'Create'

    rv = client.post("/create", data='invalid data', content_type="application/json")
    assert rv.status_code == 400
    contains = b"Failed to decode JSON object" in rv.data
    assert contains == debug

    rv = client.post("/create", data='{}', content_type="application/json")
    assert rv.status_code == 200
    assert rv.data == b'Create'
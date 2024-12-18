import pytest
import flask

def test_head_method(app, client):
    @app.route("/head", methods=["HEAD"])
    def head_route():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

    rv = client.get("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.post("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.put("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.delete("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]
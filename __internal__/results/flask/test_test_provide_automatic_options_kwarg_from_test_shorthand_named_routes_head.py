import pytest
import flask

def test_head_method(app, client):
    @app.route("/head", methods=["HEAD"])
    def head_method():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

    rv = client.get("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.post("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.delete("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]
import pytest
import flask

def test_head_method(app, client):
    @app.route("/head_test", methods=["HEAD"])
    def head_test():
        return flask.Response('', headers={'X-Method': 'HEAD'})

    rv = client.head("/head_test")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

    rv = client.get("/head_test")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.post("/head_test")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.put("/head_test")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]

    rv = client.delete("/head_test")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD", "OPTIONS"]
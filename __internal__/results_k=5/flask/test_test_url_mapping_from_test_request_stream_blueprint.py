import flask
import pytest

def test_head_method(app, client):
    class HeadView(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/head", view_func=HeadView.as_view("head_view"))

    rv = client.head("/head")
    assert rv.status_code == 200
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"

    rv = client.get("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.post("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.put("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.delete("/head")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]
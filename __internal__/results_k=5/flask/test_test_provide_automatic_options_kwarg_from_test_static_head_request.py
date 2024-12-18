import pytest
import flask

def test_head_method(app, client):
    class Index(flask.views.MethodView):
        def head(self):
            return flask.Response('', headers={'X-Method': 'HEAD'})

    app.add_url_rule("/", view_func=Index.as_view("index"))

    rv = client.head("/")
    assert rv.status_code == 200
    assert not rv.data
    assert rv.headers["X-Method"] == "HEAD"

    rv = client.get("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.post("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.delete("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["HEAD"]

    rv = client.open("/", method="OPTIONS")
    assert rv.status_code == 405

    rv = client.head("/nonexistent")
    assert rv.status_code == 404
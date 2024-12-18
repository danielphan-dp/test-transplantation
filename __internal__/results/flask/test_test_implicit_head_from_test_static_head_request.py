def test_explicit_head(app, client):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def head(self):
            return flask.Response("", headers={"X-Method": "HEAD"})

    app.add_url_rule("/", view_func=Index.as_view("index"))
    
    # Test GET request
    rv = client.get("/")
    assert rv.data == b"GET"
    
    # Test HEAD request
    rv = client.head("/")
    assert rv.data == b""
    assert rv.headers["X-Method"] == "HEAD"
    
    # Test additional headers
    rv = client.head("/")
    assert "X-Method" in rv.headers
    assert rv.headers["X-Method"] == "HEAD"
    
    # Test response status code for HEAD request
    assert rv.status_code == 200

def test_head_with_custom_header(app, client):
    class CustomHeaderView(flask.views.MethodView):
        def head(self):
            return flask.Response("", headers={"X-Custom-Header": "CustomValue"})

    app.add_url_rule("/custom", view_func=CustomHeaderView.as_view("custom_header"))
    
    rv = client.head("/custom")
    assert rv.data == b""
    assert rv.headers["X-Custom-Header"] == "CustomValue"
    assert rv.status_code == 200

def test_head_on_nonexistent_route(app, client):
    rv = client.head("/nonexistent")
    assert rv.status_code == 404
    assert rv.data == b""
import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.route("/vary-cookie-header-set")
def vary_cookie_header_set():
    response = flask.Response()
    response.vary.add("Cookie")
    flask.session["test"] = "test"
    return response

@app.route("/vary-header-set")
def vary_header_set():
    response = flask.Response()
    response.vary.update(("Accept-Encoding", "Accept-Language"))
    flask.session["test"] = "test"
    return response

@app.route("/no-vary-header")
def no_vary_header():
    return ""

def test_expect_method(client):
    def expect(path, header_value="Cookie"):
        rv = client.get(path)
        if header_value:
            assert len(rv.headers.get_all("Vary")) == 1
            assert rv.headers["Vary"] == header_value
        else:
            assert "Vary" not in rv.headers

    expect("/vary-cookie-header-set")
    expect("/vary-header-set", "Accept-Encoding, Accept-Language, Cookie")
    expect("/no-vary-header", None)

def test_expect_method_no_vary(client):
    @client.application.route("/no-vary")
    def no_vary():
        return ""

    response = client.get("/no-vary")
    assert "Vary" not in response.headers

def test_expect_method_multiple_vary(client):
    @client.application.route("/multiple-vary")
    def multiple_vary():
        response = flask.Response()
        response.vary.add("Cookie")
        response.vary.add("User-Agent")
        return response

    response = client.get("/multiple-vary")
    assert len(response.headers.get_all("Vary")) == 1
    assert response.headers["Vary"] == "Cookie"  # Only the first should be considered

def test_expect_method_empty_vary(client):
    @client.application.route("/empty-vary")
    def empty_vary():
        response = flask.Response()
        response.vary = []
        return response

    response = client.get("/empty-vary")
    assert "Vary" not in response.headers

def test_expect_method_no_cookie(client):
    @client.application.route("/no-cookie")
    def no_cookie():
        return flask.Response()

    response = client.get("/no-cookie")
    assert "Vary" not in response.headers
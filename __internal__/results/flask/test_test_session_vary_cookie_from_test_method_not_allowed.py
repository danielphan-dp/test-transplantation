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

def test_expect_function(client):
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

def test_expect_with_no_vary_header(client):
    response = client.get("/no-vary-header")
    assert "Vary" not in response.headers

def test_expect_with_multiple_vary_headers(client):
    @app.route("/multiple-vary-headers")
    def multiple_vary_headers():
        response = flask.Response()
        response.vary.add("Cookie")
        response.vary.add("User-Agent")
        return response

    response = client.get("/multiple-vary-headers")
    assert len(response.headers.get_all("Vary")) == 2
    assert "Cookie" in response.headers["Vary"]
    assert "User-Agent" in response.headers["Vary"]

def test_expect_with_empty_vary_header(client):
    @app.route("/empty-vary-header")
    def empty_vary_header():
        response = flask.Response()
        response.vary.add("")
        return response

    response = client.get("/empty-vary-header")
    assert len(response.headers.get_all("Vary")) == 1
    assert response.headers["Vary"] == ""
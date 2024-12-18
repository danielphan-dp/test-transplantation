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

def test_expect_no_vary_header(client):
    response = client.get("/no-vary-header")
    assert "Vary" not in response.headers

def test_expect_vary_header_with_multiple_values(client):
    @app.route("/vary-multiple-headers")
    def vary_multiple_headers():
        response = flask.Response()
        response.vary.update(("Accept-Encoding", "Accept-Language", "Cookie"))
        return response

    response = client.get("/vary-multiple-headers")
    assert len(response.headers.get_all("Vary")) == 1
    assert response.headers["Vary"] == "Accept-Encoding, Accept-Language, Cookie"
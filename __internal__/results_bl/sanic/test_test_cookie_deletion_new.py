import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get('/cookie')
    def get_cookie(request):
        response = text("There's a cookie up in this response")
        response.cookies['test'] = 'Cookie1'
        response.cookies['test']['httponly'] = True
        response.cookies['c2'] = 'Cookie2'
        response.cookies['c2']['httponly'] = False
        return response
    return app

def test_get_cookie(app):
    request, response = app.test_client.get('/cookie')
    
    assert response.status == 200
    assert response.text == "There's a cookie up in this response"
    assert 'test' in response.cookies
    assert response.cookies['test'] == 'Cookie1'
    assert response.cookies['test']['httponly'] is True
    assert 'c2' in response.cookies
    assert response.cookies['c2'] == 'Cookie2'
    assert response.cookies['c2']['httponly'] is False

def test_cookie_http_only(app):
    request, response = app.test_client.get('/cookie')
    
    assert response.cookies['test']['httponly'] is True
    assert response.cookies['c2']['httponly'] is False

def test_cookie_existence(app):
    request, response = app.test_client.get('/cookie')
    
    assert 'test' in response.cookies
    assert 'c2' in response.cookies

def test_cookie_deletion(app):
    cookie_jar = None

    @app.route("/")
    def handler(request):
        nonlocal cookie_jar
        response = text("OK")
        del response.cookies["one"]
        response.cookies["two"] = "testing"
        del response.cookies["two"]
        cookie_jar = response.cookies
        return response

    _, response = app.test_client.get("/")
    
    assert cookie_jar.get_cookie("one") is None
    assert cookie_jar.get_cookie("two") is None
    assert len(response.cookies) == 0
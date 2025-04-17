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
    assert 'Set-Cookie' in response.headers
    assert response.cookies['test'].value == 'Cookie1'
    assert response.cookies['test']['httponly'] is True
    assert response.cookies['c2'].value == 'Cookie2'
    assert response.cookies['c2']['httponly'] is False

def test_cookie_http_only(app):
    request, response = app.test_client.get('/cookie')
    response_cookies = response.cookies

    assert 'test' in response_cookies
    assert response_cookies['test']['httponly'] is True

def test_cookie_existence(app):
    request, response = app.test_client.get('/cookie')
    response_cookies = response.cookies

    assert response_cookies.get('test') is not None
    assert response_cookies.get('c2') is not None

def test_cookie_count(app):
    request, response = app.test_client.get('/cookie')
    response_cookies = response.cookies

    assert len(response_cookies) == 2

def test_cookie_values(app):
    request, response = app.test_client.get('/cookie')
    response_cookies = response.cookies

    assert response_cookies['test'].value == 'Cookie1'
    assert response_cookies['c2'].value == 'Cookie2'
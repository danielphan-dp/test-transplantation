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
    _, response = app.test_client.get('/cookie')
    
    assert response.status == 200
    assert response.text == "There's a cookie up in this response"
    assert 'test' in response.cookies
    assert response.cookies['test'] == 'Cookie1'
    assert response.cookies['test']['httponly'] is True
    assert 'c2' in response.cookies
    assert response.cookies['c2'] == 'Cookie2'
    assert response.cookies['c2']['httponly'] is False

def test_cookie_http_only(app):
    _, response = app.test_client.get('/cookie')
    
    assert response.cookies['test']['httponly'] is True

def test_cookie_without_http_only(app):
    _, response = app.test_client.get('/cookie')
    
    assert response.cookies['c2']['httponly'] is False

def test_no_cookies_on_empty_request(app):
    @app.get('/empty')
    def empty_handler(request):
        return text("No cookies here")

    _, response = app.test_client.get('/empty')
    
    assert len(response.cookies) == 0

def test_multiple_cookies(app):
    _, response = app.test_client.get('/cookie')
    
    assert len(response.cookies) == 2
    assert 'test' in response.cookies
    assert 'c2' in response.cookies
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_cookie(app):
    @app.get('/cookie')
    def get_cookie(request):
        response = text("There's a cookie up in this response")
        response.cookies['test'] = 'Cookie1'
        response.cookies['test']['httponly'] = True
        response.cookies['c2'] = 'Cookie2'
        response.cookies['c2']['httponly'] = False
        return response

    request, response = app.test_client.get('/cookie')
    
    assert response.text == "There's a cookie up in this response"
    assert response.cookies['test'].value == 'Cookie1'
    assert response.cookies['test']['httponly'] is True
    assert response.cookies['c2'].value == 'Cookie2'
    assert response.cookies['c2']['httponly'] is False

def test_get_cookie_no_cookies(app):
    @app.get('/empty_cookie')
    def empty_cookie(request):
        response = text("No cookies here")
        return response

    request, response = app.test_client.get('/empty_cookie')
    
    assert response.text == "No cookies here"
    assert len(response.cookies) == 0

def test_get_cookie_with_invalid_request(app):
    @app.get('/cookie')
    def get_cookie(request):
        response = text("There's a cookie up in this response")
        response.cookies['test'] = 'Cookie1'
        response.cookies['test']['httponly'] = True
        return response

    request, response = app.test_client.get('/cookie', headers={'Invalid-Header': 'value'})
    
    assert response.text == "There's a cookie up in this response"
    assert response.cookies['test'].value == 'Cookie1'
    assert response.cookies['test']['httponly'] is True

def test_get_cookie_multiple_cookies(app):
    @app.get('/multiple_cookies')
    def multiple_cookies(request):
        response = text("Multiple cookies set")
        response.cookies['cookie1'] = 'value1'
        response.cookies['cookie2'] = 'value2'
        response.cookies['cookie1']['httponly'] = True
        response.cookies['cookie2']['secure'] = True
        return response

    request, response = app.test_client.get('/multiple_cookies')
    
    assert response.cookies['cookie1'].value == 'value1'
    assert response.cookies['cookie1']['httponly'] is True
    assert response.cookies['cookie2'].value == 'value2'
    assert response.cookies['cookie2']['secure'] is True
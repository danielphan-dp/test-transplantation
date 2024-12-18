import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.get('/cookie')
def get_cookie(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'Cookie1'
    response.cookies['test']['httponly'] = True
    response.cookies['c2'] = 'Cookie2'
    response.cookies['c2']['httponly'] = False
    return response

def test_get_cookie(app):
    request, response = app.test_client.get('/cookie')
    
    assert response.status == 200
    assert response.text == "There's a cookie up in this response"
    
    response_cookies = response.cookies
    assert 'test' in response_cookies
    assert response_cookies['test'].value == 'Cookie1'
    assert response_cookies['test']['httponly'] is True
    
    assert 'c2' in response_cookies
    assert response_cookies['c2'].value == 'Cookie2'
    assert response_cookies['c2']['httponly'] is False

def test_get_cookie_no_cookies(app):
    @app.get('/no_cookies')
    def no_cookies(request):
        response = text("No cookies set")
        return response

    request, response = app.test_client.get('/no_cookies')
    
    assert response.status == 200
    assert response.text == "No cookies set"
    assert 'Set-Cookie' not in response.headers

def test_get_cookie_invalid_path(app):
    request, response = app.test_client.get('/invalid_path')
    
    assert response.status == 404

def test_get_cookie_with_custom_headers(app):
    @app.get('/custom_headers')
    def custom_headers(request):
        response = text("Custom headers test")
        response.cookies['custom'] = 'HeaderValue'
        response.cookies['custom']['httponly'] = True
        return response

    request, response = app.test_client.get('/custom_headers')
    
    assert response.status == 200
    assert response.cookies['custom'].value == 'HeaderValue'
    assert response.cookies['custom']['httponly'] is True
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
    request, response = app.test_client.get('/cookie')
    
    response_cookies = response.cookies
    assert response_cookies.get('nonexistent') is None

def test_get_cookie_with_invalid_path(app):
    request, response = app.test_client.get('/cookie', headers={"cookie": "test=invalid"})
    
    response_cookies = response.cookies
    assert response_cookies['test'].value == 'Cookie1'
    assert response_cookies['c2'].value == 'Cookie2'
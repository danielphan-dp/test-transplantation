import pytest
from sanic import Sanic
from sanic.response import text
from sanic.cookies import CookieJar

app = Sanic("TestApp")

@app.get('/cookie')
def get_cookie(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'Cookie1'
    response.cookies['test']['httponly'] = True
    response.cookies['c2'] = 'Cookie2'
    response.cookies['c2']['httponly'] = False
    return response

@pytest.fixture
def client():
    return app.test_client

def test_get_cookie(client):
    request, response = client.get('/cookie')
    assert response.status == 200
    assert response.text == "There's a cookie up in this response"
    assert 'test' in response.cookies
    assert response.cookies['test'] == 'Cookie1'
    assert response.cookies['test']['httponly'] is True
    assert 'c2' in response.cookies
    assert response.cookies['c2'] == 'Cookie2'
    assert response.cookies['c2']['httponly'] is False

def test_get_cookie_no_cookies(client):
    request, response = client.get('/cookie')
    assert response.cookies['test'] is not None
    assert response.cookies['c2'] is not None

def test_get_cookie_http_only(client):
    request, response = client.get('/cookie')
    assert response.cookies['test']['httponly'] is True

def test_get_cookie_non_existent_cookie(client):
    request, response = client.get('/cookie')
    assert response.cookies.get('non_existent') is None

def test_get_cookie_multiple_requests(client):
    request1, response1 = client.get('/cookie')
    request2, response2 = client.get('/cookie')
    assert response1.cookies['test'] == response2.cookies['test']
    assert response1.cookies['c2'] == response2.cookies['c2']
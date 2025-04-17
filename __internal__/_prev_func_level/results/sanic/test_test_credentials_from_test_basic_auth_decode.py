import base64
import pytest
from sanic import Sanic
from sanic.response import text

def encode_basic_auth_credentials(username, password):
    return base64.b64encode(f'{username}:{password}'.encode()).decode('ascii')

@pytest.mark.parametrize(('username', 'password', 'expected'), [
    ('user1', 'pass1', 'dXNlcjE6cGFzczE='),
    ('user2', 'pass2', 'dXNlcjI6cGFzczI='),
    ('', '', ':'),
    ('user3', None, 'user3:None'),
    (None, 'pass3', 'None:pass3'),
])
def test_encode_basic_auth_credentials(username, password, expected):
    assert encode_basic_auth_credentials(username, password) == expected

@pytest.mark.parametrize(('username', 'password'), [
    ('valid_user', 'valid_pass'),
    ('another_user', 'another_pass'),
])
def test_credentials_with_valid_auth(app, capfd, username, password):
    token = encode_basic_auth_credentials(username, password)
    auth_type = 'Basic'
    
    @app.route("/")
    async def handler(request):
        return text("OK")

    headers = {
        "content-type": "application/json",
        "Authorization": f"{auth_type} {token}"
    }

    request, response = app.test_client.get("/", headers=headers)

    assert request.credentials.username == username
    assert request.credentials.password == password
    assert request.credentials.auth_type == auth_type
    assert request.credentials.token == token

@pytest.mark.parametrize(('username', 'password'), [
    ('user1', 'pass1'),
    ('user2', 'pass2'),
])
def test_credentials_with_invalid_auth(app, capfd, username, password):
    token = 'invalid_token'
    auth_type = 'Bearer'
    
    @app.route("/")
    async def handler(request):
        return text("OK")

    headers = {
        "content-type": "application/json",
        "Authorization": f"{auth_type} {token}"
    }

    request, response = app.test_client.get("/", headers=headers)

    assert request.credentials is None
    assert not hasattr(request.credentials, "token")
    assert not hasattr(request.credentials, "auth_type")
    assert not hasattr(request.credentials, "_username")
    assert not hasattr(request.credentials, "_password")
import base64
import pytest
from sanic import Sanic
from sanic.response import text

def encode_basic_auth_credentials(username, password):
    return base64.b64encode(f'{username}:{password}'.encode()).decode('ascii')

@pytest.mark.parametrize(('username', 'password', 'expected'), [
    ('user1', 'pass1', encode_basic_auth_credentials('user1', 'pass1')),
    ('user2', 'pass2', encode_basic_auth_credentials('user2', 'pass2')),
    ('', '', encode_basic_auth_credentials('', '')),
    ('user3', '', encode_basic_auth_credentials('user3', '')),
    ('', 'pass3', encode_basic_auth_credentials('', 'pass3')),
])
def test_encode_basic_auth_credentials(username, password, expected):
    assert encode_basic_auth_credentials(username, password) == expected

@pytest.mark.parametrize(('username', 'password'), [
    (None, 'pass'),
    ('user', None),
    (None, None),
])
def test_encode_basic_auth_credentials_invalid(username, password):
    with pytest.raises(TypeError):
        encode_basic_auth_credentials(username, password)

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_credentials_basic_auth(app):
    @app.route("/")
    async def handler(request):
        return text("OK")

    username = 'test_user'
    password = 'test_pass'
    token = encode_basic_auth_credentials(username, password)

    headers = {
        "content-type": "application/json",
        "Authorization": f"Basic {token}"
    }

    request, response = app.test_client.get("/", headers=headers)

    assert request.credentials.username == username
    assert request.credentials.password == password
    assert request.credentials.token is None
    assert request.credentials.auth_type == "Basic"

def test_credentials_no_auth(app):
    @app.route("/")
    async def handler(request):
        return text("OK")

    headers = {"content-type": "application/json"}

    request, response = app.test_client.get("/", headers=headers)

    assert request.credentials is None
    assert not hasattr(request.credentials, "token")
    assert not hasattr(request.credentials, "auth_type")
import base64
import logging
import json
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize(('auth_type', 'token'), [
    (None, 'a1d895e0-553a-421a-8e22-5ff8ecb48cbf'),
    ('Token', 'a1d895e0-553a-421a-8e22-5ff8ecb48cbf'),
    ('Bearer', 'a1d895e0-553a-421a-8e22-5ff8ecb48cbf'),
    (None, None),
    ('InvalidType', 'invalid-token'),
    ('Token', ''),
    ('Bearer', None)
])
def test_get_method(app, auth_type, token):
    @app.route("/get")
    async def get_handler(request):
        return text('I am get method')

    if token:
        headers = {
            "content-type": "application/json",
            "Authorization": f"{auth_type} {token}" if auth_type else f"{token}",
        }
    else:
        headers = {"content-type": "application/json"}

    request, response = app.test_client.get("/get", headers=headers)
    
    assert response.text == 'I am get method'
    if token:
        assert request.token == token
    else:
        assert request.token is None
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
    (None, None),
    ('user', ''),
    ('', 'pass'),
])
def test_encode_basic_auth_credentials_edge_cases(username, password):
    with pytest.raises(TypeError):
        encode_basic_auth_credentials(username, password)
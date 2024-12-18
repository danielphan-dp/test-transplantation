import base64
import pytest
from unittest.mock import MagicMock
from connexion.exceptions import OAuthProblem
from connexion.lifecycle import ConnexionRequest
from connexion.security import NO_VALUE, OAuthSecurityHandler

def test_verify_oauth_invalid_auth_type():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"Bearer token"]]})

    assert wrapped_func(request) is NO_VALUE

def test_verify_oauth_invalid_authorization_header():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"Basic invalid_header"]]})

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_oauth_empty_user_pass():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"Basic " + base64.b64encode(b":").decode('latin1')]]})

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_oauth_correct_credentials():
    def somefunc(username, password):
        return (username, password)

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    username = "testuser"
    password = "testpass"
    credentials = f"{username}:{password}"
    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"Basic " + base64.b64encode(credentials.encode('latin1')).decode('latin1')]]})

    assert wrapped_func(request) == (username, password)
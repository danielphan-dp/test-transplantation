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

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"invalid_auth_type"]]})

    assert wrapped_func(request) is NO_VALUE

def test_verify_oauth_invalid_header_format():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"my_basic invalid_format"]]})

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_oauth_empty_user_pass():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"my_basic "]]})

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_oauth_missing_user_pass():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", b"my_basic dGVzdA=="]]})

    assert wrapped_func(request) is NO_VALUE

def test_verify_oauth_valid_credentials():
    def somefunc(username, password):
        assert username == "testuser"
        assert password == "testpass"
        return True

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    user_pass = base64.b64encode(b"testuser:testpass").decode('latin1')
    request = ConnexionRequest(scope={"type": "http", "headers": [[b"Authorization", f"my_basic {user_pass}".encode()]]})

    assert wrapped_func(request) is True
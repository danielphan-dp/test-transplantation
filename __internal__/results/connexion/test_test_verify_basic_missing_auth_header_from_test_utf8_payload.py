import base64
import pytest
from unittest.mock import MagicMock
from connexion.lifecycle import ConnexionRequest
from connexion.security import NO_VALUE, BasicSecurityHandler, OAuthProblem

def test_verify_basic_invalid_auth_type():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"InvalidAuthType dGVzdDp0ZXN0"]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_invalid_auth_header_format():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"Basic InvalidFormatHeader"]]}
    )

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_basic_empty_username_password():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    empty_credentials = base64.b64encode(b":").decode('latin1')
    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", f"Basic {empty_credentials}".encode()]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_invalid_base64_decoding():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"Basic InvalidBase64"]]}
    )

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)
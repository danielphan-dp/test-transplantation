import base64
import pytest
from unittest.mock import MagicMock
from connexion.lifecycle import ConnexionRequest
from connexion.exceptions import OAuthProblem
from connexion.security import NO_VALUE, BasicSecurityHandler

def test_verify_basic_invalid_auth_type():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"InvalidAuthType dGVzdDp0ZXN0"]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_invalid_credentials_format():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic dGVzdA=="]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_empty_credentials():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic "]]}
    )

    with pytest.raises(OAuthProblem) as exc_info:
        wrapped_func(request)

    assert exc_info.value.detail == 'Invalid authorization header'

def test_verify_basic_invalid_base64_decoding():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic invalid_base64"]]}
    )

    with pytest.raises(OAuthProblem) as exc_info:
        wrapped_func(request)

    assert exc_info.value.detail == 'Invalid authorization header'
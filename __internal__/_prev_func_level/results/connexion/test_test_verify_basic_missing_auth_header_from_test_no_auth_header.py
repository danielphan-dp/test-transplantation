import base64
import pytest
from unittest.mock import MagicMock
from connexion.exceptions import OAuthProblem
from connexion.lifecycle import ConnexionRequest
from connexion.security import NO_VALUE, BasicSecurityHandler

def test_verify_basic_invalid_auth_type():
    def somefunc(username, password):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"InvalidAuthType dGVzdDp0ZXN0"]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_invalid_auth_header_format():
    def somefunc(username, password):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic invalid_format_header"]]}
    )

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_basic_empty_user_pass():
    def somefunc(username, password):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic "]]}
    )

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)

def test_verify_basic_invalid_base64_decoding():
    def somefunc(username, password):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic invalid_base64"]]}
    )

    with pytest.raises(OAuthProblem, match="Invalid authorization header"):
        wrapped_func(request)
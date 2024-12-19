import json
import unittest.mock.MagicMock
import unittest.mock.patch
import pytest
import requests
from connexion.exceptions.BadRequestProblem import BadRequestProblem
from connexion.exceptions.ConnexionException import ConnexionException
from connexion.exceptions.OAuthProblem import OAuthProblem
from connexion.exceptions.OAuthResponseProblem import OAuthResponseProblem
from connexion.exceptions.OAuthScopeProblem import OAuthScopeProblem
from connexion.lifecycle.ConnexionRequest import ConnexionRequest
from connexion.security.NO_VALUE import NO_VALUE
from connexion.security.ApiKeySecurityHandler import ApiKeySecurityHandler
from connexion.security.BasicSecurityHandler import BasicSecurityHandler
from connexion.security.OAuthSecurityHandler import OAuthSecurityHandler
from connexion.security.SecurityHandlerFactory import SecurityHandlerFactory

def test_verify_basic_invalid_auth_type():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"Bearer 123"]]}
    )

    assert wrapped_func(request) is NO_VALUE

def test_verify_basic_invalid_auth_header_format():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic 123"]]}
    )

    with pytest.raises(OAuthProblem, match='Invalid authorization header'):
        wrapped_func(request)

def test_verify_basic_valid_auth_header():
    def somefunc(username, password, required_scopes=None):
        return (username, password)

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    username = 'user'
    password = 'pass'
    user_pass = f"{username}:{password}".encode('latin1')
    auth_header = f"my_basic {base64.b64encode(user_pass).decode('latin1')}"

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", auth_header.encode('latin1')]]}
    )

    assert wrapped_func(request) == (username, password)

def test_verify_basic_invalid_base64_decoding():
    def somefunc(username, password, required_scopes=None):
        return None

    security_handler = BasicSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(
        scope={"type": "http", "headers": [[b"authorization", b"my_basic invalid_base64"]]}
    )

    with pytest.raises(OAuthProblem, match='Invalid authorization header'):
        wrapped_func(request)
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

def test_verify_oauth_invalid_auth_type():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [("Authorization", "Bearer token")]})

    assert wrapped_func(request) is NO_VALUE

def test_verify_oauth_invalid_auth_header_format():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    request = ConnexionRequest(scope={"type": "http", "headers": [("Authorization", "my_basic invalid_format")]})

    with pytest.raises(OAuthProblem, match='Invalid authorization header'):
        wrapped_func(request)

def test_verify_oauth_missing_colon_in_credentials():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    user_pass = base64.b64encode(b'usernamewithoutcolon').decode('latin1')
    request = ConnexionRequest(scope={"type": "http", "headers": [("Authorization", f"my_basic {user_pass}")]})

    with pytest.raises(OAuthProblem, match='Invalid authorization header'):
        wrapped_func(request)

def test_verify_oauth_empty_credentials():
    def somefunc(token):
        return None

    security_handler = OAuthSecurityHandler()
    wrapped_func = security_handler._get_verify_func(somefunc)

    user_pass = base64.b64encode(b':').decode('latin1')
    request = ConnexionRequest(scope={"type": "http", "headers": [("Authorization", f"my_basic {user_pass}")]})

    with pytest.raises(OAuthProblem, match='Invalid authorization header'):
        wrapped_func(request)
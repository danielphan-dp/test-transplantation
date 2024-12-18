import base64
import json
import pytest
from connexion import App
from connexion.exceptions import OAuthProblem
from connexion.security import NO_VALUE, BasicSecurityHandler

def test_post_method_with_valid_data():
    app = App(__name__)
    app_client = app.test_client()

    res = app_client.post("/v1.0/post_endpoint", json={"key": "value"})
    assert res.status_code == 201
    assert res.json == {"key": "value", "name": "post"}

def test_post_method_with_empty_data():
    app = App(__name__)
    app_client = app.test_client()

    res = app_client.post("/v1.0/post_endpoint", json={})
    assert res.status_code == 201
    assert res.json == {"name": "post"}

def test_post_method_with_invalid_json():
    app = App(__name__)
    app_client = app.test_client()

    res = app_client.post("/v1.0/post_endpoint", data="invalid json")
    assert res.status_code == 400

def test_post_method_with_missing_key():
    app = App(__name__)
    app_client = app.test_client()

    res = app_client.post("/v1.0/post_endpoint", json={"name": "post"})
    assert res.status_code == 201
    assert res.json == {"name": "post"}

def test_post_method_with_authentication():
    class MyBasicSecurityHandler(BasicSecurityHandler):
        def _get_verify_func(self, basic_info_func):
            check_basic_info_func = self.check_basic_auth(basic_info_func)

            def wrapper(request):
                auth_type, user_pass = self.get_auth_header_value(request)
                if auth_type != "my_basic":
                    return NO_VALUE

                try:
                    username, password = (
                        base64.b64decode(user_pass).decode("latin1").split(":", 1)
                    )
                except Exception:
                    raise OAuthProblem(detail="Invalid authorization header")

                return check_basic_info_func(request, username, password)

            return wrapper

    security_map = {
        "basic": MyBasicSecurityHandler,
    }
    app = App(__name__)
    app.add_api('spec.yaml', security_map=security_map)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/post_endpoint",
        headers={"Authorization": "basic dGVzdDp0ZXN0"},
    )
    assert res.status_code == 401

    res = app_client.post(
        "/v1.0/post_endpoint",
        headers={"Authorization": "my_basic dGVzdDp0ZXN0"},
        json={"key": "value"}
    )
    assert res.status_code == 201
    assert res.json == {"key": "value", "name": "post"}
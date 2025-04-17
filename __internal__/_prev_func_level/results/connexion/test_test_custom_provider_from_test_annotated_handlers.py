import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_json_method_with_valid_json(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    valid_json = '{"key": "value"}'
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = valid_json

    response = flask_app.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_string(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    empty_json = ''
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = empty_json

    with pytest.raises(json.JSONDecodeError):
        flask_app.json()

def test_json_method_with_invalid_json(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    invalid_json = '{"key": "value"'
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = invalid_json

    with pytest.raises(json.JSONDecodeError):
        flask_app.json()
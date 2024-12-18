import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_json_method_with_valid_data(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    valid_data = '{"key": "value"}'
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = valid_data

    response = flask_app.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_data(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    empty_data = ''
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = empty_data

    response = flask_app.json()
    assert response == ''

def test_json_method_with_invalid_json(spec):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    invalid_json_data = '{"key": "value"'
    flask_app.json = FlaskJSONProvider(flask_app)
    flask_app.json.text = invalid_json_data

    with pytest.raises(json.JSONDecodeError):
        flask_app.json()
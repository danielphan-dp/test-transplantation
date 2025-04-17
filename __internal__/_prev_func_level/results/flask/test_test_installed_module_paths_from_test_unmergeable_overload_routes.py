import os
import sys
import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

def test_purge_module(purge_module, app):
    @app.route("/test")
    def test_route():
        return "Test Route"

    purge_module("test_app")

    from test_app import test_route

    assert test_route() == "Test Route"

def test_purge_non_existent_module(purge_module):
    assert sys.modules.get("non_existent_module") is None
    purge_module("non_existent_module")
    assert sys.modules.get("non_existent_module") is None

def test_multiple_purge_calls(purge_module, app):
    @app.route("/another_test")
    def another_test_route():
        return "Another Test Route"

    purge_module("another_test_app")
    from another_test_app import another_test_route

    assert another_test_route() == "Another Test Route"
    purge_module("another_test_app")
    assert sys.modules.get("another_test_app") is None

def test_purge_module_with_dependencies(purge_module, app):
    @app.route("/dependent_test")
    def dependent_test_route():
        return "Dependent Test Route"

    purge_module("dependent_test_app")
    from dependent_test_app import dependent_test_route

    assert dependent_test_route() == "Dependent Test Route"
    purge_module("dependent_test_app")
    assert sys.modules.get("dependent_test_app") is None
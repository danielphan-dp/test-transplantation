import os
import sys
import pytest
import flask

@pytest.fixture
def mock_app(purge_module):
    app = flask.Flask(__name__)
    purge_module("mock_app")
    return app

def test_purge_module_removes_app(mock_app):
    assert "mock_app" in sys.modules
    mock_app = None
    assert "mock_app" not in sys.modules

def test_purge_module_with_nonexistent_app(purge_module):
    assert "nonexistent_app" not in sys.modules
    purge_module("nonexistent_app")
    assert "nonexistent_app" not in sys.modules

def test_purge_module_multiple_calls(purge_module):
    app1 = flask.Flask("app1")
    app2 = flask.Flask("app2")
    purge_module("app1")
    purge_module("app2")
    assert "app1" not in sys.modules
    assert "app2" not in sys.modules

def test_purge_module_with_imported_app(purge_module, monkeypatch):
    app_path = os.path.join(os.path.dirname(__file__), "mock_app.py")
    with open(app_path, "w") as f:
        f.write("import flask\napp = flask.Flask(__name__)\n")
    monkeypatch.syspath_prepend(os.path.dirname(app_path))
    import mock_app
    assert "mock_app" in sys.modules
    purge_module("mock_app")
    assert "mock_app" not in sys.modules

def test_purge_module_does_not_affect_other_modules(purge_module):
    sys.modules["test_module"] = "test"
    purge_module("test_module")
    assert "test_module" not in sys.modules
    assert "os" in sys.modules  # Ensure os module is still present
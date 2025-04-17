import os
import sys
import pytest
import flask

@pytest.fixture
def app(purge_module):
    app = flask.Flask(__name__)
    purge_module("test_app")
    return app

def test_purge_module_removes_imported_module(app, modules_tmp_path):
    (modules_tmp_path / "test_app.py").write_text(
        "import flask\napp = flask.Flask(__name__)\n"
    )
    from test_app import app as imported_app
    assert imported_app.instance_path == os.fspath(
        modules_tmp_path / "var" / "test_app-instance"
    )
    
    # Purge the module
    purge_module("test_app")
    
    # Attempt to import again after purge
    with pytest.raises(ModuleNotFoundError):
        from test_app import app

def test_purge_module_multiple_calls(app, modules_tmp_path):
    (modules_tmp_path / "test_app.py").write_text(
        "import flask\napp = flask.Flask(__name__)\n"
    )
    purge_module("test_app")
    
    from test_app import app as imported_app
    assert imported_app.instance_path == os.fspath(
        modules_tmp_path / "var" / "test_app-instance"
    )
    
    # Purge the module again
    purge_module("test_app")
    
    # Check if the module can still be imported
    with pytest.raises(ModuleNotFoundError):
        from test_app import app

def test_purge_module_with_nonexistent_module(app):
    with pytest.raises(ModuleNotFoundError):
        purge_module("non_existent_module")("non_existent_module")
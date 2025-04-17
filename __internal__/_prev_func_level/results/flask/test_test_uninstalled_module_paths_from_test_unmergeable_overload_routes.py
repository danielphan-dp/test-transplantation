import os
import sys
import pytest
import flask

@pytest.fixture
def modules_tmp_path(tmp_path, monkeypatch):
    rv = tmp_path / "modules_tmp"
    rv.mkdir()
    monkeypatch.syspath_prepend(os.fspath(rv))
    return rv

def test_purge_module_functionality(modules_tmp_path, purge_module):
    (modules_tmp_path / "test_module.py").write_text(
        "def test_func():\n"
        "    return 'Hello World'\n"
    )
    purge_module("test_module")

    with pytest.raises(ModuleNotFoundError):
        from test_module import test_func

def test_purge_module_with_flask_app(modules_tmp_path, purge_module):
    (modules_tmp_path / "flask_app.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
        "@app.route('/test')\n"
        "def test_route():\n"
        "    return 'Test Successful'\n"
    )
    purge_module("flask_app")

    from flask_app import app

    with app.test_client() as client:
        response = client.get('/test')
        assert response.data == b'Test Successful'

    purge_module("flask_app")

    with pytest.raises(ModuleNotFoundError):
        from flask_app import app

def test_multiple_purge_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "another_module.py").write_text(
        "def another_func():\n"
        "    return 'Another Function'\n"
    )
    purge_module("another_module")
    purge_module("another_module")

    with pytest.raises(ModuleNotFoundError):
        from another_module import another_func

def test_purge_non_existent_module(modules_tmp_path, purge_module):
    purge_module("non_existent_module")
    assert True  # No exception should be raised for non-existent module

def test_purge_module_with_flask_app_instance_path(modules_tmp_path, purge_module):
    (modules_tmp_path / "app_instance.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("app_instance")

    from app_instance import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
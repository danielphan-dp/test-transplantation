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

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_module(modules_tmp_path, purge_module):
    app = modules_tmp_path / "test_app"
    app.mkdir()
    (app / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("test_app")

    with pytest.raises(KeyError):
        from test_app import app

def test_purge_module_does_not_remove_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_purge_module_removes_multiple_modules(modules_tmp_path, purge_module):
    app1 = modules_tmp_path / "test_app1"
    app1.mkdir()
    (app1 / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    app2 = modules_tmp_path / "test_app2"
    app2.mkdir()
    (app2 / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    
    purge_module("test_app1")
    purge_module("test_app2")

    with pytest.raises(KeyError):
        from test_app1 import app
    with pytest.raises(KeyError):
        from test_app2 import app

def test_purge_module_with_existing_import(modules_tmp_path, purge_module):
    app = modules_tmp_path / "config_package_app"
    app.mkdir()
    (app / "__init__.py").write_text(
        "import os\n"
        "import flask\n"
        "here = os.path.abspath(os.path.dirname(__file__))\n"
        "app = flask.Flask(__name__)\n"
    )
    from config_package_app import app
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
    purge_module("config_package_app")
    
    with pytest.raises(KeyError):
        from config_package_app import app

def test_purge_module_with_flask_app(modules_tmp_path, purge_module):
    app = modules_tmp_path / "flask_app"
    app.mkdir()
    (app / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("flask_app")
    
    with pytest.raises(KeyError):
        from flask_app import app

def test_purge_module_edge_case_empty_name(modules_tmp_path, purge_module):
    with pytest.raises(TypeError):
        purge_module("")
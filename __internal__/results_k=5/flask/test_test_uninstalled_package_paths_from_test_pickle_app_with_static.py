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
        import test_app

def test_purge_module_does_not_remove_nonexistent_module(modules_tmp_path, purge_module):
    purge_module("nonexistent_module")
    assert "nonexistent_module" not in sys.modules

def test_purge_module_removes_multiple_modules(modules_tmp_path, purge_module):
    app1 = modules_tmp_path / "app1"
    app1.mkdir()
    (app1 / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    
    app2 = modules_tmp_path / "app2"
    app2.mkdir()
    (app2 / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    
    purge_module("app1")
    purge_module("app2")

    with pytest.raises(KeyError):
        import app1
    with pytest.raises(KeyError):
        import app2

def test_purge_module_with_imported_app(modules_tmp_path, purge_module):
    app = modules_tmp_path / "imported_app"
    app.mkdir()
    (app / "__init__.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("imported_app")

    from imported_app import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
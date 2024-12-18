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

def test_purge_uninstalled_module(modules_tmp_path, purge_module):
    (modules_tmp_path / "test_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("test_module")

    with pytest.raises(ModuleNotFoundError):
        from test_module import app

def test_purge_module_with_multiple_imports(modules_tmp_path, purge_module):
    (modules_tmp_path / "multi_import_module.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("multi_import_module")

    from multi_import_module import app
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")

def test_purge_non_existent_module(modules_tmp_path, purge_module):
    non_existent_module = "non_existent_module"
    purge_module(non_existent_module)

    with pytest.raises(ModuleNotFoundError):
        __import__(non_existent_module)

def test_purge_module_after_import(modules_tmp_path, purge_module):
    (modules_tmp_path / "temp_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    from temp_module import app
    assert app is not None
    purge_module("temp_module")
    
    with pytest.raises(ModuleNotFoundError):
        from temp_module import app

def test_purge_module_with_app_instance(modules_tmp_path, purge_module):
    (modules_tmp_path / "app_instance_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("app_instance_module")

    from app_instance_module import app
    assert app.instance_path == os.fspath(modules_tmp_path / "instance")
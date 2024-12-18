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
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("test_module")

    with pytest.raises(ModuleNotFoundError):
        from test_module import app

def test_purge_module_with_instance_path(modules_tmp_path, purge_module):
    (modules_tmp_path / "instance_module.py").write_text(
        "import os\n"
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module("instance_module")

    from instance_module import app

    assert app.instance_path == os.fspath(modules_tmp_path / "instance")

def test_multiple_purge_calls(modules_tmp_path, purge_module):
    (modules_tmp_path / "first_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    (modules_tmp_path / "second_module.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    
    purge_module("first_module")
    purge_module("second_module")

    from first_module import app as first_app
    from second_module import app as second_app

    assert first_app.instance_path == os.fspath(modules_tmp_path / "instance")
    assert second_app.instance_path == os.fspath(modules_tmp_path / "instance")
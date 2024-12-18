import os
import pytest
import flask

@pytest.fixture
def purge_module(request):
    def inner(name):
        request.addfinalizer(lambda: sys.modules.pop(name, None))
    return inner

def test_purge_module_removes_module(modules_tmp_path, purge_module):
    module_name = "test_module"
    app = modules_tmp_path / module_name
    app.mkdir()
    (app / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module(module_name)

    with pytest.raises(ModuleNotFoundError):
        from test_module import app

def test_purge_module_does_not_remove_other_modules(modules_tmp_path, purge_module):
    module_name = "test_module"
    other_module_name = "other_module"
    app = modules_tmp_path / module_name
    other_app = modules_tmp_path / other_module_name
    app.mkdir()
    other_app.mkdir()
    (app / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    (other_app / "__init__.py").write_text(
        "import flask\n"
        "other_app = flask.Flask(__name__)\n"
    )
    purge_module(module_name)

    from other_module import other_app
    assert other_app.name == "other_module"

def test_purge_module_with_nonexistent_module(modules_tmp_path, purge_module):
    nonexistent_module_name = "nonexistent_module"
    purge_module(nonexistent_module_name)

    with pytest.raises(ModuleNotFoundError):
        from nonexistent_module import app

def test_purge_module_multiple_calls(modules_tmp_path, purge_module):
    module_name = "test_module"
    app = modules_tmp_path / module_name
    app.mkdir()
    (app / "__init__.py").write_text(
        "import flask\n"
        "app = flask.Flask(__name__)\n"
    )
    purge_module(module_name)
    purge_module(module_name)

    with pytest.raises(ModuleNotFoundError):
        from test_module import app

def test_purge_module_edge_case_empty_name(modules_tmp_path, purge_module):
    with pytest.raises(ValueError):
        purge_module("")
import os
import sys
import pytest
import flask

@pytest.fixture
def mock_app(purge_module, modules_tmp_path, site_packages):
    app = site_packages / "mock_app"
    app.mkdir()
    (app / "__init__.py").write_text("import flask\napp = flask.Flask(__name__)\n")
    purge_module("mock_app")
    import mock_app
    return mock_app

def test_mock_app_instance_path(mock_app, modules_tmp_path):
    assert mock_app.app.instance_path == os.fspath(
        modules_tmp_path / "var" / "mock_app-instance"
    )

def test_purge_module_removes_app(mock_app, purge_module):
    assert "mock_app" in sys.modules
    purge_module("mock_app")
    assert "mock_app" not in sys.modules

def test_purge_module_multiple_calls(mock_app, purge_module):
    purge_module("mock_app")
    assert "mock_app" not in sys.modules
    purge_module("mock_app")  # Call again to ensure no error occurs
    assert "mock_app" not in sys.modules

def test_purge_module_with_nonexistent_module(purge_module):
    purge_module("nonexistent_module")  # Should not raise an error
    assert "nonexistent_module" not in sys.modules

def test_mock_app_import_after_purge(mock_app, purge_module):
    purge_module("mock_app")
    with pytest.raises(ModuleNotFoundError):
        import mock_app  # Should raise an error since it was purged
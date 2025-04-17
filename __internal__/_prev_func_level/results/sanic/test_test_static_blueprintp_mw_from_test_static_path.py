import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'symlink', 'hard_link'])
def test_get_file_path(app: Sanic, static_file_directory, file_name):
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

@pytest.mark.parametrize('file_name', ['non_existent.file', '', '   '])
def test_get_file_path_edge_cases(app: Sanic, static_file_directory, file_name):
    if file_name == 'non_existent.file':
        with pytest.raises(FileNotFoundError):
            get_file_path(static_file_directory, file_name)
    else:
        expected_path = os.path.join(static_file_directory, file_name.strip())
        assert get_file_path(static_file_directory, file_name) == expected_path

def test_static_file_with_edge_cases(app: Sanic, static_file_directory):
    bp = Blueprint(name="test_mw", url_prefix="")
    bp.static("/edge_case.file", get_file_path(static_file_directory, "test.file"), strict_slashes=True, name="static")
    app.blueprint(bp)

    uri = app.url_for("test_mw.static")
    assert uri == "/edge_case.file"

    _, response = app.test_client.get("/edge_case.file")
    assert response.status == 200

def test_static_file_with_empty_name(app: Sanic, static_file_directory):
    bp = Blueprint(name="test_mw", url_prefix="")
    bp.static("/empty_name.file", get_file_path(static_file_directory, " "), strict_slashes=True, name="static")
    app.blueprint(bp)

    uri = app.url_for("test_mw.static")
    assert uri == "/empty_name.file"

    _, response = app.test_client.get("/empty_name.file")
    assert response.status == 200

def test_static_file_with_symlink(app: Sanic, static_file_directory):
    symlink_name = "symlink"
    os.symlink(os.path.join(static_file_directory, "test.file"), os.path.join(static_file_directory, symlink_name))

    bp = Blueprint(name="test_mw", url_prefix="")
    bp.static("/symlink.file", get_file_path(static_file_directory, symlink_name), strict_slashes=True, name="static")
    app.blueprint(bp)

    uri = app.url_for("test_mw.static")
    assert uri == "/symlink.file"

    _, response = app.test_client.get("/symlink.file")
    assert response.status == 200

    os.remove(os.path.join(static_file_directory, symlink_name))
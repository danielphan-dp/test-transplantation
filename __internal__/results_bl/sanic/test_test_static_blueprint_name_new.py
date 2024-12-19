import os
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound

@pytest.mark.parametrize('file_name', ['test.file', 'another.file', '', 'file with spaces.txt'])
def test_get_file_path(static_file_directory, file_name):
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_empty_directory():
    static_file_directory = ''
    file_name = 'test.file'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_get_file_path_invalid_file_name(static_file_directory):
    file_name = None
    with pytest.raises(TypeError):
        get_file_path(static_file_directory, file_name)

def test_get_file_path_with_special_characters(static_file_directory):
    file_name = 'file@#$.txt'
    expected_path = os.path.join(static_file_directory, file_name)
    assert get_file_path(static_file_directory, file_name) == expected_path

def test_static_blueprint_not_found(static_file_directory):
    app = Sanic("app")
    bp = Blueprint(name="static", url_prefix="/static", strict_slashes=False)
    bp.static("/test.file/", get_file_path(static_file_directory, 'test.file'), name="static.testing", strict_slashes=True)
    app.blueprint(bp)

    _, response = app.test_client.get("/static/nonexistent.file")
    assert response.status == 404

def test_static_blueprint_with_empty_file_name(static_file_directory):
    app = Sanic("app")
    bp = Blueprint(name="static", url_prefix="/static", strict_slashes=False)
    bp.static("/test.file/", get_file_path(static_file_directory, ''), name="static.testing", strict_slashes=True)
    app.blueprint(bp)

    _, response = app.test_client.get("/static/test.file/")
    assert response.status == 200

def test_static_blueprint_with_spaces(static_file_directory):
    app = Sanic("app")
    bp = Blueprint(name="static", url_prefix="/static", strict_slashes=False)
    bp.static("/file with spaces.txt/", get_file_path(static_file_directory, 'file with spaces.txt'), name="static.testing", strict_slashes=True)
    app.blueprint(bp)

    _, response = app.test_client.get("/static/file%20with%20spaces.txt/")
    assert response.status == 200
import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'non_existent.file'])
def test_get_file_path(static_file_directory, file_name):
    app = Sanic("test_app")
    
    # Test valid file path
    if file_name != 'non_existent.file':
        app.static("/testing.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
    
    # Test non-existent file path
    else:
        with pytest.raises(FileNotFoundError):
            app.static("/testing.file", get_file_path(static_file_directory, file_name))
            app.test_client.get("/testing.file")

    # Test with a blueprint
    bp = Blueprint("test_bp", url_prefix="/bp")
    bp.static("/testing.file", get_file_path(static_file_directory, file_name))
    app.blueprint(bp)

    request, response = app.test_client.get("/bp/testing.file")
    if file_name != 'non_existent.file':
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
    else:
        with pytest.raises(FileNotFoundError):
            app.test_client.get("/bp/testing.file")
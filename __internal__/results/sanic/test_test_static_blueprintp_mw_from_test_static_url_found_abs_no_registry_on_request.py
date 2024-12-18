import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound

@pytest.mark.parametrize('file_name', ['test.file', 'non_existent.file'])
def test_get_file_path(app: Sanic, static_file_directory, file_name):
    bp = Blueprint(name="test_mw", url_prefix="")
    
    if file_name == 'non_existent.file':
        with pytest.raises(NotFound):
            app.static("/test.file", get_file_path(static_file_directory, file_name))
            app.test_client.get("/test.file")
    else:
        app.static("/test.file", get_file_path(static_file_directory, file_name))
        uri = app.url_for("test_mw.static")
        assert uri == "/test.file"
        
        request, response = app.test_client.get("/test.file")
        assert response.status == 200
        assert response.body is not None  # Assuming the file exists and has content

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_get_file_path_with_special_characters(app: Sanic, static_file_directory, file_name):
    app.static("/test.file", get_file_path(static_file_directory, file_name))
    uri = app.url_for("test_mw.static")
    assert uri == "/test.file"
    
    request, response = app.test_client.get("/test.file")
    assert response.status == 200
    assert response.body is not None  # Assuming the file exists and has content

def test_get_file_path_invalid_directory(app: Sanic):
    invalid_directory = "/invalid/directory"
    file_name = "test.file"
    with pytest.raises(NotFound):
        app.static("/test.file", get_file_path(invalid_directory, file_name))
        app.test_client.get("/test.file")
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

    # Test with different static file directory
    new_static_directory = os.path.join(static_file_directory, "new_static")
    app.static("/new_testing.file", get_file_path(new_static_directory, file_name))
    if file_name != 'non_existent.file':
        request, response = app.test_client.get("/new_testing.file")
        assert response.status == 200
        assert response.body == get_file_content(new_static_directory, file_name)
    
    # Test for URL generation with external server
    uri = app.url_for("static", _external=True, _server="http://localhost")
    assert uri == f"http://localhost/testing.file" if file_name != 'non_existent.file' else f"http://localhost/new_testing.file"
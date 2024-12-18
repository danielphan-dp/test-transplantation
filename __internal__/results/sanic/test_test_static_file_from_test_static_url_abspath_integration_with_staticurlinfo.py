import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png', 'non_existent.file'])
def test_get_file_path(static_file_directory, file_name):
    app = Sanic("test_app")
    
    # Test valid file path
    if file_name != 'non_existent.file':
        app.static("/valid.file", get_file_path(static_file_directory, file_name))
        request, response = app.test_client.get("/valid.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
    
    # Test non-existent file path
    else:
        with pytest.raises(FileNotFoundError):
            app.static("/invalid.file", get_file_path(static_file_directory, file_name))
            request, response = app.test_client.get("/invalid.file")
    
    # Test with absolute path
    absolute_path = os.path.abspath(get_file_path(static_file_directory, file_name))
    if os.path.exists(absolute_path):
        app.static("/absolute.file", absolute_path)
        request, response = app.test_client.get("/absolute.file")
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)
    
    # Test with different static file directory
    new_static_directory = os.path.join(static_file_directory, "new_static")
    app.static("/new_static.file", get_file_path(new_static_directory, file_name))
    request, response = app.test_client.get("/new_static.file")
    assert response.status == 200
    assert response.body == get_file_content(new_static_directory, file_name) if os.path.exists(get_file_path(new_static_directory, file_name)) else response.status == 404

    # Test for URL generation with external server
    uri = app.url_for("static", _external=True, _server="http://localhost")
    assert uri == f"http://localhost/valid.file" if file_name != 'non_existent.file' else uri == f"http://localhost/invalid.file"
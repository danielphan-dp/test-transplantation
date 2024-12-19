import os
import pytest
from sanic import Sanic
from sanic.exceptions import FileNotFound

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt", "non_existent.file"])
def test_get_file_path(app, static_file_directory, file_name):
    if file_name == "non_existent.file":
        with pytest.raises(FileNotFound):
            get_file_path(static_file_directory, file_name)
    else:
        path = get_file_path(static_file_directory, file_name)
        assert os.path.join(static_file_directory, file_name) == path

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_valid_names(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_pathlib_with_valid_names(app, static_file_directory, file_name):
    from pathlib import Path
    file_path = Path(get_file_path(static_file_directory, file_name))
    app.static("/testing.file", file_path)
    request, response = app.test_client.get("/testing.file")
    assert response.status == 200

@pytest.mark.parametrize("file_name", ["test.file", "decode me.txt"])
def test_static_file_with_invalid_range(app, static_file_directory, file_name):
    app.static("/testing.file", get_file_path(static_file_directory, file_name), use_content_range=True)
    headers = {"Range": "bytes=-"}
    request, response = app.test_client.get("/testing.file", headers=headers)
    assert response.status == 416
    assert "Invalid for Content Range parameters" in response.text
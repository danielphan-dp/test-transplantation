import os
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound

@pytest.mark.parametrize('file_name', ['test.file', '', 'invalid/file.name', 'another_test.file'])
def test_get_file_path(app: Sanic, static_file_directory, file_name):
    if file_name == '':
        expected_path = os.path.join(static_file_directory, '')
    else:
        expected_path = os.path.join(static_file_directory, file_name)

    assert get_file_path(static_file_directory, file_name) == expected_path

@pytest.mark.parametrize('file_name', ['test.file', 'non_existent.file'])
def test_static_blueprint_invalid_file(app: Sanic, static_file_directory, file_name):
    bp = Blueprint(name="test_mw", url_prefix="")
    
    bp.static(
        "/test.file",
        get_file_path(static_file_directory, file_name),
        strict_slashes=True,
        name="static",
    )

    app.blueprint(bp)

    if file_name == 'non_existent.file':
        with pytest.raises(NotFound):
            app.test_client.get("/test.file")
    else:
        _, response = app.test_client.get("/test.file")
        assert response.status == 200
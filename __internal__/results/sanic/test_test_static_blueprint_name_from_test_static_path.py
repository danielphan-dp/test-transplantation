import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound

@pytest.mark.parametrize('file_name', ['test.file', 'non_existent.file', 'another_test.file'])
def test_get_file_path(static_file_directory, file_name):
    app = Sanic("app")
    bp = Blueprint(name="static", url_prefix="/static", strict_slashes=False)

    file_path = get_file_path(static_file_directory, file_name)
    
    if file_name == 'non_existent.file':
        assert not os.path.exists(file_path)
    else:
        assert os.path.exists(file_path)

    bp.static(
        f"/{file_name}/",
        file_path,
        name="static.testing",
        strict_slashes=True,
    )

    app.blueprint(bp)

    uri = app.url_for("static", name="static.testing")
    assert uri == f"/static/{file_name}/"

    _, response = app.test_client.get(f"/static/{file_name}")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200

    _, response = app.test_client.get(f"/static/{file_name}/")
    if file_name == 'non_existent.file':
        assert response.status == 404
    else:
        assert response.status == 200
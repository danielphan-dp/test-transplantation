import os
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import NotFound

@pytest.mark.parametrize('file_name', ['test.html', 'non_existent_file.html', '', 'valid_file.txt'])
def test_get_file_path(app, file_name):
    current_file = inspect.getfile(inspect.currentframe())
    current_directory = os.path.dirname(os.path.abspath(current_file))
    static_directory = os.path.join(current_directory, "static")

    blueprint = Blueprint("test_static")
    file_path = get_file_path(static_directory, file_name)

    if file_name == 'non_existent_file.html':
        with pytest.raises(NotFound):
            app.test_client.get(f"/{file_name}")
    else:
        blueprint.static(
            f"/{file_name}",
            file_path,
            content_type="text/html; charset=utf-8",
        )
        app.blueprint(blueprint)

        request, response = app.test_client.get(f"/{file_name}")
        if file_name == '':
            assert response.status == 404
        else:
            assert response.status == 200
            assert response.body == get_file_content(static_directory, file_name)
            assert response.headers["Content-Type"] == "text/html; charset=utf-8"
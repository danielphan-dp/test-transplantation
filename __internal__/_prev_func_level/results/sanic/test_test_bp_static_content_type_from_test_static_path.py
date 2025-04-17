import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.html', 'non_existent_file.html'])
def test_get_file_path(app, file_name):
    current_file = inspect.getfile(inspect.currentframe())
    current_directory = os.path.dirname(os.path.abspath(current_file))
    static_directory = os.path.join(current_directory, "static")

    blueprint = Blueprint("test_static")
    
    if file_name == 'non_existent_file.html':
        with pytest.raises(FileNotFoundError):
            blueprint.static(
                "/testing.file",
                get_file_path(static_directory, file_name),
                content_type="text/html; charset=utf-8",
            )
    else:
        blueprint.static(
            "/testing.file",
            get_file_path(static_directory, file_name),
            content_type="text/html; charset=utf-8",
        )

        app.blueprint(blueprint)

        request, response = app.test_client.get("/testing.file")
        assert response.status == 200
        assert response.body == get_file_content(static_directory, file_name)
        assert response.headers["Content-Type"] == "text/html; charset=utf-8"
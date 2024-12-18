import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'non_existent.file', 'decode me.txt'])
def test_get_file_path(app: Sanic, static_file_directory, file_name):
    bp = Blueprint(name="test_mw", url_prefix="")
    
    @bp.route("/get_file_path")
    def get_file_path_route(request):
        return text(get_file_path(static_file_directory, file_name))

    app.blueprint(bp)

    if file_name == 'non_existent.file':
        response = app.test_client.get("/get_file_path")
        assert response.status == 404
    else:
        response = app.test_client.get("/get_file_path")
        expected_path = os.path.join(static_file_directory, file_name)
        assert response.text == expected_path
        assert response.status == 200

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_static_file_with_edge_cases(app: Sanic, static_file_directory, file_name):
    app.static("/static/" + file_name, get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/static/" + file_name)
    if file_name == 'test.file':
        assert response.status == 200
    else:
        assert response.status == 404

@pytest.mark.parametrize('file_name', ['test.file', 'symlink', 'hard_link'])
def test_static_file_with_symlinks(app: Sanic, static_file_directory, file_name):
    app.static("/symlink_test/" + file_name, get_file_path(static_file_directory, file_name))

    request, response = app.test_client.get("/symlink_test/" + file_name)
    assert response.status == 200
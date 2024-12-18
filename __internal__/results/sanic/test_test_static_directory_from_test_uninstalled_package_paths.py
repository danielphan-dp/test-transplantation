import os
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint

@pytest.fixture(autouse=True)
def reset():
    try:
        del os.environ['SANIC_MOTD_OUTPUT']
    except KeyError:
        pass

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'non_existent.file'])
@pytest.mark.parametrize('base_uri', ['/static', '', '/dir', '/invalid'])
def test_static_directory_with_edge_cases(file_name, base_uri, static_file_directory):
    app = Sanic("base")
    app.static(base_uri, static_file_directory)
    base_uri2 = base_uri + "/2"
    app.static(base_uri2, static_file_directory, name="uploads")

    uri = app.url_for("static", name="static", filename=file_name)
    
    if file_name == 'non_existent.file':
        with pytest.raises(Exception):
            app.test_client.get(uri)
    else:
        assert uri == f"{base_uri}/{file_name}"
        request, response = app.test_client.get(uri)
        assert response.status == 200
        assert response.body == get_file_content(static_file_directory, file_name)

    uri2 = app.url_for("static", name="static", filename="/" + file_name)
    uri3 = app.url_for("static", filename=file_name)
    uri4 = app.url_for("static", filename="/" + file_name)
    uri5 = app.url_for("static", name="uploads", filename=file_name)
    uri6 = app.url_for("static", name="uploads", filename="/" + file_name)

    assert uri == uri2
    assert uri2 == uri3
    assert uri3 == uri4

    assert uri5 == f"{base_uri2}/{file_name}"
    assert uri5 == uri6

    bp = Blueprint("test_bp_static", url_prefix="/bp")
    bp.static(base_uri, static_file_directory)
    bp.static(base_uri2, static_file_directory, name="uploads")

    app.router.reset()
    app.blueprint(bp)

    uri = app.url_for("static", name="test_bp_static.static", filename=file_name)
    uri2 = app.url_for("static", name="test_bp_static.static", filename="/" + file_name)
    uri4 = app.url_for("static", name="test_bp_static.uploads", filename=file_name)
    uri5 = app.url_for("static", name="test_bp_static.uploads", filename="/" + file_name)

    assert uri == f"/bp{base_uri}/{file_name}"
    assert uri == uri2
    assert uri4 == f"/bp{base_uri2}/{file_name}"
    assert uri4 == uri5

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)
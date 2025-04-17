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

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_static_file_with_edge_cases(static_file_directory, file_name):
    app = Sanic("qq")
    app.static("/testing.file", get_file_path(static_file_directory, file_name))
    app.static("/testing2.file", get_file_path(static_file_directory, file_name), name="testing_file")
    app.router.finalize()

    uri = app.url_for("static")
    uri2 = app.url_for("static", filename="any")
    uri3 = app.url_for("static", name="static", filename="any")

    assert uri == "/testing.file"
    assert uri == uri2
    assert uri2 == uri3

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    app.router.reset()

    bp = Blueprint("test_bp_static", url_prefix="/bp")
    bp.static("/testing.file", get_file_path(static_file_directory, file_name))
    bp.static("/testing2.file", get_file_path(static_file_directory, file_name), name="testing_file")
    app.blueprint(bp)

    uris = [
        app.url_for("static", name="test_bp_static.static"),
        app.url_for("static", name="test_bp_static.static", filename="any"),
        app.url_for("test_bp_static.static"),
        app.url_for("test_bp_static.static", filename="any"),
    ]

    assert all(uri == "/bp/testing.file" for uri in uris)

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    uri = app.url_for("static", _external=True, _server="http://localhost")
    assert uri == "http://localhost/testing.file"

    uri = app.url_for("static", name="test_bp_static.static", _external=True, _server="http://localhost")
    assert uri == "http://localhost/bp/testing.file"

    uri = app.url_for("static", name="testing_file")
    assert uri == "/testing2.file"

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    uri = app.url_for("static", name="test_bp_static.testing_file")
    assert uri == "/bp/testing2.file"
    assert uri == app.url_for("static", name="test_bp_static.testing_file", filename="any")

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.body == get_file_content(static_file_directory, file_name)

    # Additional edge case: Test with non-existent file
    non_existent_uri = app.url_for("static", filename="non_existent.file")
    request, response = app.test_client.get(non_existent_uri)
    assert response.status == 404

    # Additional edge case: Test with invalid name
    invalid_name_uri = app.url_for("static", name="invalid_name")
    request, response = app.test_client.get(invalid_name_uri)
    assert response.status == 404
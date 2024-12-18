import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_head_request(file_name, static_file_directory):
    app = Sanic("test_app")
    uri = f"/testing.file"

    request, response = app.test_client.head(uri)
    assert response.status == 200
    assert response.headers['method'] == 'HEAD'
    assert 'Content-Length' in response.headers
    assert int(response.headers['Content-Length']) == 0

    # Test with non-existing file
    non_existing_uri = "/non_existing.file"
    request, response = app.test_client.head(non_existing_uri)
    assert response.status == 404

    # Test with invalid method
    request, response = app.test_client.get(uri)
    assert response.status == 405
    assert 'method' not in response.headers

    # Test with additional headers
    request, response = app.test_client.head(uri, headers={'Custom-Header': 'value'})
    assert response.status == 200
    assert response.headers['method'] == 'HEAD'
    assert response.headers['Custom-Header'] == 'value'
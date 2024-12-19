import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/static', '/nonexistent'])
def test_get_method(app: Sanic, request_path: str):
    if request_path == '/static':
        app.static("static", Path(static_file_directory) / 'test.file')
        _, response = app.test_client.get(request_path)
        assert response.status == 200
        assert response.body == b'I am get method'
    else:
        _, response = app.test_client.get(request_path)
        assert response.status == 404
        assert response.body == b''

def test_get_method_no_path(app: Sanic):
    _, response = app.test_client.get('')
    assert response.status == 404
    assert response.body == b''

def test_get_method_invalid_method(app: Sanic):
    _, response = app.test_client.post('/static')
    assert response.status == 405
    assert response.body == b''
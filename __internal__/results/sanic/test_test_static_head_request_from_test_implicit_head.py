import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('url', ['/nonexistent', '/another/nonexistent'])
def test_head_request_not_found(app, url):
    request, response = app.test_client.head(url)
    assert response.status == 404

def test_head_request_empty_response(app):
    @app.route('/empty', methods=['HEAD'])
    async def empty_response(request):
        return text('', headers={'method': 'HEAD'})

    request, response = app.test_client.head('/empty')
    assert response.status == 200
    assert response.data == b''
    assert response.headers['method'] == 'HEAD'
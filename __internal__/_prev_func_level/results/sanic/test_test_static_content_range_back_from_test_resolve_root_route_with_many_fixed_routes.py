import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/'])
def test_get_method_response(app, path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)

    assert response.status == 200
    assert response.text == 'I am get method'
    assert 'Content-Length' in response.headers
    assert int(response.headers['Content-Length']) == len(response.text)
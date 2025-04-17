import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_method', ['GET', 'POST'])
def test_get_method_response(app, request_method):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')

    if request_method == 'GET':
        request, response = app.test_client.get('/get')
    else:
        request, response = app.test_client.post('/get')

    assert response.status == 200
    assert response.text == 'I am get method'
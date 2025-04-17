import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('request_path', ["/", "/nonexistent"])
def test_get_method(app, request_path):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, request_path)

    request, response = app.test_client.get(request_path)

    if request_path == "/":
        assert response.status == 200
        assert response.text == 'I am get method'
    else:
        assert response.status == 404
        assert "Requested URL" in response.text
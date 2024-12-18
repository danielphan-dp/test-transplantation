import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_path', ['/test', '/another_test'])
def test_get_method(request_path):
    app = Sanic("test_app")

    @app.get(request_path)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(request_path)
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test for a non-existing route
    request, response = app.test_client.get('/non_existing')
    assert response.status == 404

    # Test for method not allowed
    request, response = app.test_client.post(request_path)
    assert response.status == 405
    assert "Method POST not allowed for URL" in response.text
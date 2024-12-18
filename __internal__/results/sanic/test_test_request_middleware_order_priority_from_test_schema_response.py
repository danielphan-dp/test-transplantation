import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize("expected_status", [200, 500])
def test_get_method_response(app: Sanic, expected_status):
    @app.get("/test_get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get")
    
    if expected_status == 200:
        assert response.status == 200
        assert response.text == "I am get method"
    else:
        # Simulate an error scenario (not applicable in this case, but for coverage)
        assert response.status == 500, response.text

def test_get_method_no_request(app: Sanic):
    @app.get("/test_get_no_request")
    def get_method(request):
        return text('I am get method without request')

    request, response = app.test_client.get("/test_get_no_request")
    assert response.status == 200
    assert response.text == "I am get method without request"
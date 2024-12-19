import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('request_data', [
    {'path': '/test', 'expected_body': 'I am get method', 'expected_status': 200},
    {'path': '/invalid', 'expected_body': 'Not Found', 'expected_status': 404},
])
def test_get_method(app: Sanic, request_data):
    @app.route("/test", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get(request_data['path'])
    assert response.body.decode() == request_data['expected_body']
    assert response.status == request_data['expected_status']
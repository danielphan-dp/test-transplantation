import pytest
from datetime import datetime, timedelta
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('max_age', ['-1', 'invalid', None])
def test_get_method_with_invalid_max_age(app, max_age):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'
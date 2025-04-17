import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or OS_IS_WINDOWS, reason='Not testable with current client')
def test_get_method(port):
    app = Sanic("test_app")

    @app.get("/test")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    
    assert response.status == 200
    assert response.text == "I am get method"
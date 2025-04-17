import pytest
from sanic.response import text

@pytest.mark.parametrize('test_str', ['sanic-test', 'sanictest', 'sanic test'])
def test_get_method(app, test_str):
    @app.route("/api/v1/test/")
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/api/v1/test/")
    
    assert response.status == 200
    assert response.text == "I am get method"
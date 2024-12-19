import pytest
from urllib.parse import quote
from sanic.response import text

@pytest.mark.parametrize('test_str', ['sanic-test', 'sanictest', 'sanic test', '', '123', 'special@chars!'])
def test_get_method(app, test_str):
    @app.route("/api/v1/test/<test>/")
    async def init_handler(request, test):
        return text('I am get method')

    _, response = app.test_client.get(f"/api/v1/test/{quote(test_str)}/")
    
    assert response.status == 200
    assert response.body == b'I am get method'
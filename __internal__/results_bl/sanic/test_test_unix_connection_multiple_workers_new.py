import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_get_method_response():
    app = Sanic(name="test_get_method")
    
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_get_method_invalid_route():
    app = Sanic(name="test_get_method_invalid_route")
    
    @app.get("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

@pytest.mark.skipif(sys.platform not in ('linux', 'darwin'), reason='This test requires fork context')
def test_get_method_with_query_params():
    app = Sanic(name="test_get_method_query_params")
    
    @app.get("/")
    async def handler(request):
        return text(f'I am get method with params: {request.args}')

    request, response = app.test_client.get("/?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == 'I am get method with params: MultiDict([(\'param1\', [\'value1\']), (\'param2\', [\'value2\'])])'
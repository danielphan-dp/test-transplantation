import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('url', ['/get', '/get/'])
def test_get_method(app, url):
    """Test the GET method of the DummyView."""
    
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, url)
    
    request, response = app.test_client.get(url)
    
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('invalid_url', ['/invalid', '/not_found'])
def test_get_method_invalid_url(app, invalid_url):
    """Test GET method with invalid URLs."""
    
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, '/get')
    
    request, response = app.test_client.get(invalid_url)
    
    assert response.status == 404
    assert "Requested URL" in response.text

def test_get_method_with_query_params(app):
    """Test GET method with query parameters."""
    
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param value is {param}')

    app.add_route(DummyView().get, '/get_with_param')
    
    request, response = app.test_client.get('/get_with_param?param=test_value')
    
    assert response.status == 200
    assert response.text == 'Param value is test_value'

def test_get_method_without_query_params(app):
    """Test GET method without query parameters."""
    
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param value is {param}')

    app.add_route(DummyView().get, '/get_with_param')
    
    request, response = app.test_client.get('/get_with_param')
    
    assert response.status == 200
    assert response.text == 'Param value is default'
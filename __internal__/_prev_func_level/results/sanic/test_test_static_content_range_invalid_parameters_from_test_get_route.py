import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/'])
def test_get_method(app, path):
    request, response = app.test_client.get(path)
    
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.parametrize('path', ['/invalid'])
def test_get_method_invalid_path(app, path):
    request, response = app.test_client.get(path)
    
    assert response.status == 404
    assert "Requested URL" in response.text

@pytest.mark.parametrize('path', ['/'])
def test_get_method_with_middleware(app, path):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    request, response = app.test_client.get(path)

    assert response.text == 'I am get method'
    assert len(results) == 1
    assert results[0].path == path

@pytest.mark.parametrize('path', ['/'])
def test_get_method_with_custom_class_methods(app, path):
    class DummyView:
        global_var = 0

        def get(self, request):
            self.global_var += 10
            return text(f'I am get method and global var is {self.global_var}')

    app.add_route(DummyView().get, path)
    request, response = app.test_client.get(path)

    assert response.text == 'I am get method and global var is 10'
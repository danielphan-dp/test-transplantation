import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.parametrize('path', ['/valid_path', '/another_valid_path', '/invalid_path'])
def test_get_method(app, path):
    """Test the GET method of the DummyView with various paths."""
    
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, path)

    request, response = app.test_client.get(path)

    if path in ['/valid_path', '/another_valid_path']:
        assert response.status == 200
        assert response.text == 'I am get method'
    else:
        assert response.status == 404
        assert "Requested URL" in response.text
import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text
from sanic_testing import SanicTestClient

@pytest.mark.parametrize('name,expected', (
    ('url_for', '/url-for'),
))
def test_url_for_route_name(app, name, expected):
    """Tests that the url_for route is named correctly."""
    event = asyncio.Event()

    @app.route('/url-for', name='url_for')
    async def url_for_route(request):
        event.set()
        return text('url-for')

    uri = app.url_for(name)
    assert uri == expected
    request, response = SanicTestClient(app).get(uri)
    assert response.status == 200
    assert response.text == 'url-for'
    assert event.is_set()

def test_fails_if_endpoint_not_found(app):
    """Tests that an error is raised if the endpoint is not found."""
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_route")
        assert "Endpoint with name `non_existent_route` was not found" in str(e.value)

def test_url_for_with_query_params(app):
    """Tests url_for with query parameters."""
    @app.route('/url-for', methods=['GET'])
    async def url_for_route(request):
        return text('url-for')

    uri = app.url_for('url_for', param1='value1', param2='value2')
    assert uri == '/url-for?param1=value1&param2=value2'
    request, response = SanicTestClient(app).get(uri)
    assert response.status == 200
    assert response.text == 'url-for'
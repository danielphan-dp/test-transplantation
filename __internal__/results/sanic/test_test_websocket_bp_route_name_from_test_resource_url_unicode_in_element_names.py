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
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    uri = app.url_for(name)
    assert uri == expected

    request, response = SanicTestClient(app).get(uri)
    assert response.status == 200
    assert response.text == 'url-for'

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_route")
        assert str(e.value) == "Endpoint with name `non_existent_route` was not found"

def test_url_for_with_query_params(app):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    uri = app.url_for('url_for', param1='value1', param2='value2')
    assert uri == '/url-for?param1=value1&param2=value2'

    request, response = SanicTestClient(app).get(uri)
    assert response.status == 200
    assert response.text == 'url-for'
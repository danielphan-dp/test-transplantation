import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.exceptions import URLBuildError
from sanic.response import text

def test_url_for_method():
    app = Sanic("app")
    
    @app.route('/url-for', methods=['GET'])
    def url_for(request):
        return text('url-for')

    @app.get("/get", name="route_get")
    def handler(request):
        return text("OK")

    @app.get("/another-route", name="another_route")
    def another_handler(request):
        return text("Another OK")

    assert app.url_for("route_get") == "/get"
    assert app.url_for("another_route") == "/another-route"
    
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")
    
    response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'
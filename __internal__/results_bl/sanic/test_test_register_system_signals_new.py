import asyncio
import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(os.name == 'nt', reason='May hang CI on py38/windows')
@pytest.mark.asyncio
async def test_get_method(app):
    """Test the GET method of the Sanic application"""
    
    @app.route("/get")
    async def get_route(request):
        return text('I am get method')

    request, response = await app.test_client.get('/get')
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.skipif(os.name == 'nt', reason='May hang CI on py38/windows')
@pytest.mark.asyncio
async def test_get_method_not_found(app):
    """Test the GET method for a non-existent route"""
    
    request, response = await app.test_client.get('/non_existent')
    assert response.status == 404
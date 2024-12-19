import asyncio
import os
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.skipif(os.name == 'nt', reason='May hang CI on py38/windows')
def test_get_method(app):
    """Test the GET method of the Sanic application"""
    
    @app.route("/get")
    async def get_route(request):
        return await app.get(request)

    request = MagicMock()
    response = asyncio.run(get_route(request))
    
    assert response.status == 200
    assert response.body.decode() == 'I am get method'
import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import URLBuildError
from sanic.response import text

app = Sanic("app")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

def test_url_for_route():
    request = None  # Mock request if necessary
    response = url_for(request)
    assert response.body == b'url-for'
    assert response.status == 200

def test_url_for_invalid_route():
    with pytest.raises(URLBuildError):
        app.url_for("non_existent_route")
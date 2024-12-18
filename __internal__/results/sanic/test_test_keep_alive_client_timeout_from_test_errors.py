import asyncio
import pytest
from sanic import Sanic
from sanic.response import text
from sanic_testing.reusable import ReusableClient

@pytest.mark.skipif(bool(os.environ.get('SANIC_NO_UVLOOP')) or platform.system() != 'Linux', reason='Not testable with current client')
def test_get_method(port):
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get(request):
        return text("I am get method")

    client = ReusableClient(app, port=port)

    request, response = client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

    # Test with additional headers
    headers = {"Custom-Header": "Test"}
    request, response = client.get("/test", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("Custom-Header") is None  # No custom header in response

    # Test with invalid route
    request, response = client.get("/invalid")
    assert response.status == 404

    # Test with method not allowed
    request, response = client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text

    # Test with keep-alive connection
    loops = 0
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            with client:
                request, response = client.get("/test", headers={"Connection": "keep-alive"})
                assert response.status == 200
                assert response.text == "I am get method"
                loop.run_until_complete(asyncio.sleep(2))
                request, response = client.get("/test")
                assert response.status == 200
                assert response.text == "I am get method"
        except OSError:
            loops += 1
            if loops > 5:
                raise
            continue
        else:
            break
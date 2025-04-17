import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('override', (True, False))
def test_post_method_response(override):
    app = Sanic("Test")

    @app.post("/post")
    async def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/post", debug=True)
    assert response.status == 200
    assert response.text == 'I am post method'

    # Testing with different request methods
    rv = app.test_client.get("/post")
    assert rv.status == 405
    assert "Method GET not allowed for URL /post" in rv.text

    rv = app.test_client.put("/post")
    assert rv.status == 405
    assert "Method PUT not allowed for URL /post" in rv.text

    rv = app.test_client.delete("/post")
    assert rv.status == 405
    assert "Method DELETE not allowed for URL /post" in rv.text

    # Testing with invalid URL
    rv = app.test_client.post("/invalid")
    assert rv.status == 404
    assert "Requested URL /invalid not found" in rv.text
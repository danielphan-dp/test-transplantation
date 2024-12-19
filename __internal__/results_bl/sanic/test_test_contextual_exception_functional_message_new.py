import logging
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

app = Sanic("Test")

def test_post_method():
    @app.post("/test_post")
    async def post_method(request):
        return text('I am post method')

    _, response = app.test_client.post("/test_post")
    assert response.status == 200
    assert response.text == 'I am post method'

@pytest.mark.parametrize('override', (True, False))
def test_contextual_exception_functional_message(override):
    class TeapotError(SanicException):
        status_code = 418

        @property
        def message(self):
            return f"Received foo={self.context['foo']}"

    @app.post("/coffee", error_format="json")
    async def make_coffee(_):
        error_args = {"context": {"foo": "bar"}}
        if override:
            error_args["message"] = "override"
        raise TeapotError(**error_args)

    _, response = app.test_client.post("/coffee", debug=True)
    error_message = "override" if override else "Received foo=bar"
    assert response.status == 418
    assert response.json["message"] == error_message
    assert response.json["context"] == {"foo": "bar"}

def test_post_method_with_invalid_data():
    @app.post("/test_post_invalid")
    async def post_method_invalid(request):
        return text('Invalid data', status=400)

    _, response = app.test_client.post("/test_post_invalid", json={"invalid": "data"})
    assert response.status == 400
    assert response.text == 'Invalid data'
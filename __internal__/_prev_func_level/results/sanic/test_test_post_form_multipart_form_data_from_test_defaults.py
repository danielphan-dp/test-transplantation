import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('payload', [
    '------sanic\r\nContent-Disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n',
    '------sanic\r\ncontent-disposition: form-data; name="test"\r\n\r\nOK\r\n------sanic--\r\n'
])
def test_get_method(app, payload):
    @app.route("/", methods=["GET"])
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert request.method == 'GET'
    assert request.path == '/'
    assert request.headers.get('Content-Type') is None
    assert request.content_length == 0
    assert request.params.get('test') is None
    assert request.GET.get('test') is None
    assert request.POST.get('test') is None
    assert request.cookies.get('type') is None
    assert request.path_info == '/'
    assert request.script_name == ''
    assert request.path_qs == ''
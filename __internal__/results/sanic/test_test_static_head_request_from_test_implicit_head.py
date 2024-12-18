import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_head_request(file_name, static_file_directory):
    app = Sanic("test_app")
    
    @app.route("/head_test", methods=["HEAD"])
    def head_test(request):
        return text('', headers={'method': 'HEAD'})

    uri = "/head_test"
    
    request, response = app.test_client.head(uri)
    assert response.status == 200
    assert response.data == b''
    assert response.headers['method'] == 'HEAD'
import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('proxy', ['', 'proxy', 'servername'])
def test_url_for_with_server_name(app: Sanic, proxy: str):
    app.config.SERVER_NAME = f"{proxy}.example.com" if proxy else ""
    
    @app.route('/url-for')
    def url_for(request: Request):
        return text('url-for')

    expected_url = f"http://{proxy}.example.com/url-for" if proxy else "http://127.0.0.1/url-for"
    
    request, response = app.test_client.get('/url-for')
    assert response.status == 200
    assert response.text == 'url-for'
    assert app.url_for('url_for', _external=True) == expected_url

def test_url_for_endpoint_not_found(app: Sanic):
    with pytest.raises(Exception) as e:
        app.url_for("non_existent_endpoint")
        assert "Endpoint with name `non_existent_endpoint` was not found" in str(e.value)

def test_url_for_with_additional_params(app: Sanic):
    @app.route('/url-for/<param>')
    def url_for_with_param(request: Request, param):
        return text(f'url-for with param: {param}')

    request, response = app.test_client.get('/url-for/test')
    assert response.status == 200
    assert response.text == 'url-for with param: test'
    assert app.url_for('url_for_with_param', param='test', _external=True) == 'http://127.0.0.1/url-for/test'
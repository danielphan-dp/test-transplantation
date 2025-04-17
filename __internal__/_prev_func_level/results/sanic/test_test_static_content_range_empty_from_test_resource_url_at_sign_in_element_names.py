import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
def test_url_for_method(app, file_name):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    uri = app.url_for('url_for')
    assert uri == '/url-for'
    
    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'url-for'

    # Test with additional parameters
    uri_with_params = app.url_for('url_for', param1='value1', param2='value2')
    assert uri_with_params == '/url-for?param1=value1&param2=value2'
    
    request_with_params, response_with_params = app.test_client.get(uri_with_params)
    assert response_with_params.status == 200
    assert response_with_params.text == 'url-for'

    # Test for non-existing endpoint
    with pytest.raises(Exception) as e:
        app.url_for('non_existing_view')
        assert str(e.value) == "Endpoint with name `non_existing_view` was not found"
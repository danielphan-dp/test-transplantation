import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt', 'python.png'])
def test_url_for_with_different_parameters(static_file_directory, file_name):
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    app.router.finalize()

    # Test basic URL generation
    uri = app.url_for('url_for')
    assert uri == '/url-for'

    # Test URL generation with external parameters
    uri_external = app.url_for('url_for', _external=True, _server='http://localhost')
    assert uri_external == 'http://localhost/url-for'

    # Test URL generation with additional query parameters
    uri_with_query = app.url_for('url_for', param1='value1', param2='value2')
    assert uri_with_query == '/url-for?param1=value1&param2=value2'

    # Test URL generation with a non-existent endpoint
    with pytest.raises(Exception) as e:
        app.url_for('non_existent_endpoint')
        assert "Endpoint with name `non_existent_endpoint` was not found" in str(e.value)

    # Test URL generation with a blueprint
    bp = Blueprint("test_bp", url_prefix="/bp")
    app.blueprint(bp)

    @bp.route('/url-for')
    def bp_url_for(request):
        return text('bp-url-for')

    app.router.finalize()

    uri_bp = app.url_for('test_bp.bp_url_for')
    assert uri_bp == '/bp/url-for'

    uri_bp_external = app.url_for('test_bp.bp_url_for', _external=True, _server='http://localhost')
    assert uri_bp_external == 'http://localhost/bp/url-for'

    # Test URL generation with a defined name
    uri_defined_name = app.url_for('url_for', name='url_for')
    assert uri_defined_name == '/url-for'

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'url-for'
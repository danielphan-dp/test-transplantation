import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_endpoint_override_with_invalid_method(app):
    app.debug = True

    class Index(flask.views.View):
        methods = ["GET", "POST"]

        def dispatch_request(self):
            return flask.request.method

    app.add_url_rule("/", view_func=Index.as_view("index"))

    with pytest.raises(AssertionError):
        app.add_url_rule("/", view_func=Index.as_view("index"))

    # Test for invalid method
    response = app.test_client().put('/')
    assert response.status_code == 405

    # Test for OPTIONS method
    meths = parse_set_header(app.test_client().open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['GET', 'HEAD', 'OPTIONS', 'POST']

    # Additional test for HEAD method
    head_response = app.test_client().head('/')
    assert head_response.status_code == 200
    assert head_response.data == b''

    # Test for a non-existent route
    non_existent_response = app.test_client().get('/non-existent')
    assert non_existent_response.status_code == 404

    common_test(app)
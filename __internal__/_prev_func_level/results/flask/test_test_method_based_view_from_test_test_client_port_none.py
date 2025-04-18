import pytest
from werkzeug.http import parse_set_header
import flask.views

def test_method_based_view_with_edge_cases(app):
    class Index(flask.views.MethodView):
        def get(self):
            return "GET"

        def post(self):
            return "POST"

        def delete(self):
            return "DELETE"

    app.add_url_rule("/", view_func=Index.as_view("index"))

    c = app.test_client()
    
    # Test GET request
    response = c.get('/')
    assert response.data == b'GET'
    
    # Test POST request
    response = c.post('/')
    assert response.data == b'POST'
    
    # Test DELETE request
    response = c.delete('/')
    assert response.status_code == 405  # Method Not Allowed
    
    # Test PUT request
    response = c.put('/')
    assert response.status_code == 405  # Method Not Allowed
    
    # Test OPTIONS request
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST']
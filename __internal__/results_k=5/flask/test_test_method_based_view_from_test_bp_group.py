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
    
    # Test GET method
    response = c.get('/')
    assert response.data == b'GET'
    
    # Test POST method
    response = c.post('/')
    assert response.data == b'POST'
    
    # Test DELETE method
    response = c.delete('/')
    assert response.status_code == 405  # Method not allowed
    
    # Test PUT method
    response = c.put('/')
    assert response.status_code == 405  # Method not allowed
    
    # Test OPTIONS method
    meths = parse_set_header(c.open('/', method='OPTIONS').headers['Allow'])
    assert sorted(meths) == ['DELETE', 'GET', 'HEAD', 'OPTIONS', 'POST']
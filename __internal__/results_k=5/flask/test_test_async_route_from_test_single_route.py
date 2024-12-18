import pytest
from flask import Flask, request

@pytest.mark.parametrize('path', ['/', '/home', '/bp/', '/view', '/methodview'])
def test_post_method(path, async_app):
    app = Flask(__name__)
    app.add_url_rule(path, 'post_route', lambda: 'Create', methods=['POST'])
    test_client = async_app.test_client()
    
    response = test_client.post(path)
    assert response.data == b'Create'
    
    response = test_client.get(path)
    assert b'GET' not in response.get_data()  # Ensure GET is not allowed on POST route

    response = test_client.post(path, data={'invalid': 'data'})
    assert response.data == b'Create'  # Ensure POST still works with invalid data

    response = test_client.post(path, data={})
    assert response.data == b'Create'  # Ensure POST works with empty data
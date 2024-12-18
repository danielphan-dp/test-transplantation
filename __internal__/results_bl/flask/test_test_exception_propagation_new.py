import pytest
from flask import Flask, session

@pytest.mark.parametrize('key', ['TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None])
def test_get_method(app, client, key):
    app.testing = False
    if key is not None:
        app.config[key] = True

    with app.test_request_context():
        session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

    with app.test_request_context():
        session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
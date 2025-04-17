import pytest
from flask import Flask, session

@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_value(app, client, session_value, expected):
    with app.test_request_context():
        session['value'] = session_value
        response = client.get('/get')
        assert response.data.decode() == expected

def test_get_value_without_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
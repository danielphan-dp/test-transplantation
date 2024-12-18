import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.mark.parametrize('value, expected', [
    (None, b'None'),
    ('test_value', b'test_value'),
])
def test_get_value(value, expected):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = value
        response = client.get('/get')
        assert response.data == expected

def test_get_no_value():
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'
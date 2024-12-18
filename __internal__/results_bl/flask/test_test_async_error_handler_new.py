import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.mark.parametrize('path', ['/get'])
@pytest.mark.parametrize('session_value, expected', [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_value(session_value, expected, path, async_app):
    with async_app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = session_value
        response = client.get(path)
        assert response.data.decode() == expected

@pytest.mark.parametrize('path', ['/get'])
def test_get_value_no_session(async_app, path):
    with async_app.test_client() as client:
        response = client.get(path)
        assert response.data.decode() == 'None'
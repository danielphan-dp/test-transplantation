import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.mark.parametrize('value, expected', [
    (None, 'None'),
    ('test_value', 'test_value'),
    ('', ''),
])
def test_get_value(monkeypatch, value, expected):
    with app.test_request_context():
        session['value'] = value
        assert get() == expected

@pytest.mark.parametrize('value', [
    None,
    'test_value',
    '',
])
def test_get_value_no_session(monkeypatch, value):
    with app.test_request_context():
        assert get() == 'None'
import datetime
import pytest
import flask
from werkzeug.http import http_date

@pytest.mark.parametrize('value', [
    datetime.datetime(1973, 3, 11, 6, 30, 45),
    datetime.date(1975, 1, 5),
    None,
    'test_string',
    123,
    flask.session.get('value', 'None')
])
def test_get_value(app, client, value):
    with app.test_request_context():
        flask.session['value'] = value
        r = client.get('/get')
        if value is None:
            assert r.data.decode() == 'None'
        else:
            assert r.data.decode() == str(value)
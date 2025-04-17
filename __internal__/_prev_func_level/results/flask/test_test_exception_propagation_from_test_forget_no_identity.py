import pytest
import flask

@pytest.mark.parametrize('key', ['TESTING', 'PROPAGATE_EXCEPTIONS', 'DEBUG', None])
def test_get_session_value(app, client, key):
    app.testing = False
    if key is not None:
        app.config[key] = True

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    response = client.get('/get')
    assert response.data.decode() == 'test_value'

    with client.session_transaction() as session:
        session.clear()

    response = client.get('/get')
    assert response.data.decode() == 'None'
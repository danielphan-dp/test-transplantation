def test_get_value_from_session(app, client):
    @app.route('/set', methods=['POST'])
    def set_value():
        flask.session['value'] = 'test_value'
        return '', 204

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default session value
    response = client.get('/get')
    assert response.data == b'None'

    # Set a value in the session
    client.post('/set')
    
    # Test getting the set session value
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_with_no_session(app, client):
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Ensure no session value returns default
    response = client.get('/get')
    assert response.data == b'None'
def test_get_value(app):
    with app.test_client() as c:
        # Test when session value is not set
        rv = c.get('/get')
        assert rv.data == b'None'

        # Test when session value is set
        with c.session_transaction() as sess:
            sess['value'] = 'Test Value'
        rv = c.get('/get')
        assert rv.data == b'Test Value'

        # Test when session value is set to an empty string
        with c.session_transaction() as sess:
            sess['value'] = ''
        rv = c.get('/get')
        assert rv.data == b''

        # Test when session value is set to None
        with c.session_transaction() as sess:
            sess['value'] = None
        rv = c.get('/get')
        assert rv.data == b'None'
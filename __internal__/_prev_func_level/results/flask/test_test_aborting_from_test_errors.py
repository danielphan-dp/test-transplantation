def test_get_value(app):
    with app.test_client() as c:
        # Test default session value
        rv = c.get('/get')
        assert rv.data == b'None'

        # Test setting a session value
        with c.session_transaction() as sess:
            sess['value'] = 'Test Value'
        
        rv = c.get('/get')
        assert rv.data == b'Test Value'

        # Test clearing the session
        with c.session_transaction() as sess:
            sess.clear()
        
        rv = c.get('/get')
        assert rv.data == b'None'
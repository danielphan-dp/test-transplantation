import logging
import pytest
from flask import session
from blueprintapp import app

def test_get_value_from_session(test_apps, monkeypatch):
    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get('/get')
        assert response.data.decode() == 'None'

        # Test setting a value in session
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        
        response = c.get('/get')
        assert response.data.decode() == 'test_value'

        # Test clearing the session
        with c.session_transaction() as sess:
            sess.clear()
        
        response = c.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_with_nonexistent_key(test_apps, monkeypatch):
    with app.test_client() as c:
        # Test getting a value that does not exist in session
        response = c.get('/get')
        assert response.data.decode() == 'None'
import os
import pytest
import flask

called = []

def test_close_method(app, req_ctx):
    # Arrange
    instance = flask.Flask(__name__)
    
    # Act
    instance.close()
    
    # Assert
    assert called == [42]

def test_close_method_multiple_calls(app, req_ctx):
    # Arrange
    instance = flask.Flask(__name__)
    
    # Act
    instance.close()
    instance.close()
    
    # Assert
    assert called == [42, 42]

def test_close_method_no_calls(app, req_ctx):
    # Arrange
    instance = flask.Flask(__name__)
    
    # Act
    # No close call
    
    # Assert
    assert called == []
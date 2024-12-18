import pytest
from flask import Flask

called = []

def test_close_method_invokes_called():
    app = Flask(__name__)
    app.close()
    assert called == [42]

def test_close_method_multiple_calls():
    app = Flask(__name__)
    app.close()
    app.close()
    assert called == [42, 42]

def test_close_method_no_calls():
    assert called == []
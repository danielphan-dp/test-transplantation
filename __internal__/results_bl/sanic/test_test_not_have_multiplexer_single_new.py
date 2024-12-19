import sys
import multiprocessing
import os
from unittest.mock import Mock
import pytest
from sanic import Sanic
from sanic.worker.multiplexer import WorkerMultiplexer

def test_stop_method_without_multiplexer(app: Sanic):
    app.stop = Mock()
    app.m = None
    app.shared_ctx = Mock()
    
    stop(app)
    
    app.stop.assert_called_once()

def test_stop_method_with_multiplexer(app: Sanic):
    app.stop = Mock()
    app.m = WorkerMultiplexer()
    app.shared_ctx = Mock()
    
    stop(app)
    
    app.stop.assert_called_once()
    assert app.shared_ctx.event.is_set() is False

def test_stop_method_with_event_set(app: Sanic):
    event = multiprocessing.Event()
    app.stop = Mock()
    app.m = None
    app.shared_ctx = Mock()
    app.shared_ctx.event = event
    event.set()
    
    stop(app)
    
    app.stop.assert_called_once()
    assert event.is_set() is True

def test_stop_method_with_multiple_calls(app: Sanic):
    app.stop = Mock()
    app.m = None
    app.shared_ctx = Mock()
    
    stop(app)
    stop(app)
    
    assert app.stop.call_count == 2
import asyncio
import os
import signal
import pytest
from types import SimpleNamespace

def test_stop_method():
    """Test the stop method of the app"""

    class MockApp:
        def __init__(self):
            self.state = SimpleNamespace()
            self.state.is_stopping = False

        def stop(self):
            assert not self.state.is_stopping
            self.state.is_stopping = True

    app = MockApp()

    # Test stopping the app
    stop(app)
    assert app.state.is_stopping

    # Test calling stop again does not change state
    app.state.is_stopping = True
    stop(app)
    assert app.state.is_stopping

    # Test with a mock that simulates an exception during stop
    class ExceptionMockApp:
        def stop(self):
            raise Exception("Forced exception during stop")

    exception_app = ExceptionMockApp()
    with pytest.raises(Exception):
        stop(exception_app)
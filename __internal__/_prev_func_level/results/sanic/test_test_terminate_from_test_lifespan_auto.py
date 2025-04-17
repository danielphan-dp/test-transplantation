import os
import signal
from unittest.mock import Mock, patch
import pytest
from sanic.worker.process import terminate

@pytest.mark.parametrize("flags, expected_signal", [
    (0, signal.SIGTERM),
    (1, signal.CTRL_BREAK_EVENT)
])
@patch('sanic.worker.process.os')
def test_terminate(os_mock: Mock, flags, expected_signal):
    process = Mock()
    process.send_signal = Mock()
    context = Mock()
    context.Process.return_value = process
    global flags
    flags = flags

    terminate(process)

    if flags:
        process.send_signal.assert_called_once_with(expected_signal)
    else:
        os_mock.kill.assert_called_once_with(process.pid, expected_signal)
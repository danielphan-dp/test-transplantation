import os
import signal
from unittest.mock import Mock, patch
import pytest
from sanic.worker.manager import WorkerManager

@pytest.mark.parametrize("use_ctrl_break", [True, False])
def test_terminate_with_signal(os_mock: Mock, use_ctrl_break):
    process = Mock()
    process.pid = 1234
    context = Mock()
    context.Process.return_value = process
    manager = WorkerManager(1, Mock(), {}, context, (Mock(), Mock()), {})
    
    if use_ctrl_break:
        with patch('sanic.worker.process.CTRL_BREAK_EVENT', new=signal.CTRL_BREAK_EVENT):
            manager.terminate()
            os_mock.send_signal.assert_called_once_with(process, signal.CTRL_BREAK_EVENT)
    else:
        manager.terminate()
        os_mock.kill.assert_called_once_with(1234, signal.SIGINT)
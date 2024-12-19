import logging
import signal
from unittest.mock import Mock, patch
import pytest
from sanic.worker.manager import WorkerManager

@patch('sanic.worker.process.os')
def test_shutdown_no_process(os_mock: Mock):
    manager = WorkerManager(1, Mock(), {}, Mock(), (Mock(), Mock()), {})
    manager.shutdown()
    os_mock.kill.assert_not_called()

@patch('sanic.worker.process.os')
def test_shutdown_process_not_alive(os_mock: Mock):
    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = False
    context = Mock()
    context.Process.return_value = process
    manager = WorkerManager(1, Mock(), {}, context, (Mock(), Mock()), {})
    manager.shutdown()
    os_mock.kill.assert_not_called()

@patch('sanic.worker.process.os')
def test_shutdown_with_signal(os_mock: Mock):
    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = True
    context = Mock()
    context.Process.return_value = process
    manager = WorkerManager(1, Mock(), {}, context, (Mock(), Mock()), {})
    manager.shutdown()
    os_mock.kill.assert_called_once_with(1234, signal.SIGINT)

@patch('sanic.worker.process.os')
def test_shutdown_multiple_calls(os_mock: Mock):
    process = Mock()
    process.pid = 1234
    process.is_alive.return_value = True
    context = Mock()
    context.Process.return_value = process
    manager = WorkerManager(1, Mock(), {}, context, (Mock(), Mock()), {})
    manager.shutdown()
    manager.shutdown()
    os_mock.kill.assert_called_once_with(1234, signal.SIGINT)
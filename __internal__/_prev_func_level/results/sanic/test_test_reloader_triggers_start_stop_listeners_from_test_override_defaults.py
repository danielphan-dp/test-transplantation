import signal
import pytest
from unittest.mock import Mock
from sanic.app import Sanic
from sanic.worker.loader import AppLoader
from sanic.worker.reloader import Reloader

@pytest.fixture
def app_loader():
    return Mock(spec=AppLoader)

@pytest.fixture
def app():
    return Sanic("test_app")

def test_reloader_stops_after_timeout(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"]

def test_reloader_does_not_stop_without_signal(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    reloader.run = True  # Simulate that the reloader is running

    run_reloader(reloader)

    assert results == ["reload_process_start"]
    assert reloader.run is True

def test_reloader_with_multiple_signals(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    signal.signal(signal.SIGALRM, lambda *_: reloader.stop())
    signal.alarm(1)  # Trigger stop after 1 second

    run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"]
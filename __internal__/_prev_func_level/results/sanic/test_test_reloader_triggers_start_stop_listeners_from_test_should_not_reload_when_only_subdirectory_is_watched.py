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

def test_reloader_stops_after_timeout(app, app_loader):
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

def test_reloader_does_not_trigger_stop_if_not_running(app, app_loader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    reloader.run = False  # Simulate that the reloader is not running
    run_reloader(reloader)

    assert results == ["reload_process_start"]

def test_reloader_triggers_multiple_starts_and_stops(app, app_loader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    for _ in range(3):
        run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"] * 3

def test_reloader_signals_handling(app, app_loader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    signal.signal(signal.SIGALRM, lambda *_: reloader.stop())
    run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"]
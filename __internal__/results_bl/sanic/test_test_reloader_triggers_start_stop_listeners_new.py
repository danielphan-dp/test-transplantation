import signal
import time
import pytest
from unittest.mock import Mock
from sanic.app import Sanic
from sanic.worker.loader import AppLoader
from sanic.worker.reloader import Reloader

def test_reloader_does_not_trigger_without_start_listener(app: Sanic, app_loader: AppLoader):
    results = []
    
    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    run_reloader(reloader)

    assert results == []

def test_reloader_triggers_only_start_listener(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    run_reloader(reloader)

    assert results == ["reload_process_start"]

def test_reloader_triggers_multiple_starts_and_stops(app: Sanic, app_loader: AppLoader):
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

def test_reloader_with_long_running_process(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")
        time.sleep(2)  # Simulate long-running process

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"]

def test_reloader_stops_on_signal(app: Sanic, app_loader: AppLoader):
    results = []

    @app.reload_process_start
    def reload_process_start(_):
        results.append("reload_process_start")

    @app.reload_process_stop
    def reload_process_stop(_):
        results.append("reload_process_stop")

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    
    signal.signal(signal.SIGALRM, lambda signum, frame: reloader.stop())
    signal.alarm(1)  # Trigger the stop after 1 second

    run_reloader(reloader)

    assert results == ["reload_process_start", "reload_process_stop"]
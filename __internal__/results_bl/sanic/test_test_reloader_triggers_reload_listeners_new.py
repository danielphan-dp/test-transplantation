import signal
import pytest
from unittest.mock import Mock
from sanic.app import Sanic
from sanic.worker.loader import AppLoader
from sanic.worker.reloader import Reloader
from asyncio import Event

def test_reloader_does_not_trigger_when_no_changes(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return False  # Simulate no changes

    @app.before_reload_trigger
    async def before_reload_trigger(_):
        before.set()

    @app.after_reload_trigger
    async def after_reload_trigger(_, changed):
        after.set()
        changed_files.update(changed)

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert not before.is_set()
    assert not after.is_set()
    assert len(changed_files) == 0

def test_reloader_stops_on_signal(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return True  # Simulate changes

    @app.before_reload_trigger
    async def before_reload_trigger(_):
        before.set()

    @app.after_reload_trigger
    async def after_reload_trigger(_, changed):
        after.set()
        changed_files.update(changed)

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    reloader.check_file = check_file  # type: ignore

    # Simulate sending a signal to stop the reloader
    signal.signal(signal.SIGALRM, lambda *args: reloader.stop())
    run_reloader(reloader)

    assert before.is_set()
    assert not after.is_set()
    assert len(changed_files) == 0

def test_reloader_with_multiple_changes(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return True  # Simulate changes

    @app.before_reload_trigger
    async def before_reload_trigger(_):
        before.set()

    @app.after_reload_trigger
    async def after_reload_trigger(_, changed):
        after.set()
        changed_files.update(changed)

    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    reloader.check_file = check_file  # type: ignore
    reloader.files = lambda: ['file1.py', 'file2.py']  # Simulate multiple changed files
    run_reloader(reloader)

    assert before.is_set()
    assert after.is_set()
    assert len(changed_files) == 2
    assert changed_files == {'file1.py', 'file2.py'}
import signal
import pytest
from unittest.mock import Mock
from sanic.app import Sanic
from sanic.worker.loader import AppLoader
from sanic.worker.reloader import Reloader
from asyncio import Event

@pytest.fixture
def app_loader():
    return Mock(spec=AppLoader)

@pytest.fixture
def app():
    return Sanic("test_app")

def test_reloader_stops_after_timeout(app: Sanic, app_loader: AppLoader):
    reloader = Reloader(Mock(), 0.1, set(), app_loader)
    
    def check_file(filename, mtimes):
        return False  # Simulate no file changes

    reloader.check_file = check_file  # type: ignore
    run_reloader(reloader)

    assert not reloader.run  # Ensure reloader has stopped

def test_reloader_does_not_trigger_without_changes(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return False  # Simulate no file changes

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

def test_reloader_triggers_before_and_after_events(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return True  # Simulate file change

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

    assert before.is_set()
    assert after.is_set()
    assert len(changed_files) > 0
    assert changed_files == set(reloader.files())  # Ensure changed files are tracked correctly

def test_reloader_with_multiple_file_changes(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    changed_files = set()

    def check_file(filename, mtimes):
        return True  # Simulate multiple file changes

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

    assert before.is_set()
    assert after.is_set()
    assert len(changed_files) > 0
    assert len(changed_files) == len(reloader.files())  # Ensure all files are tracked

def test_reloader_stops_on_signal(app: Sanic, app_loader: AppLoader):
    reloader = Reloader(Mock(), 0.1, set(), app_loader)

    def check_file(filename, mtimes):
        return False  # Simulate no file changes

    reloader.check_file = check_file  # type: ignore
    signal.signal(signal.SIGALRM, lambda *_: reloader.stop())
    signal.alarm(1)  # Set alarm to stop reloader

    run_reloader(reloader)

    assert not reloader.run  # Ensure reloader has stopped after signal

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
    return Sanic("TestApp")

def test_reloader_stops_after_timeout(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    reloader = Reloader(Mock(), 0.1, set(), app_loader)

    def check_file(filename, mtimes):
        return not after.is_set()

    reloader.check_file = check_file  # type: ignore

    def stop_reloader():
        after.set()

    signal.signal(signal.SIGALRM, lambda *args: stop_reloader())
    signal.alarm(1)

    run_reloader(reloader)

    assert before.is_set()  # Ensure before trigger was called
    assert after.is_set()   # Ensure after trigger was called

def test_reloader_does_not_trigger_on_no_changes(app: Sanic, app_loader: AppLoader):
    before = Event()
    after = Event()
    reloader = Reloader(Mock(), 0.1, set(), app_loader)

    def check_file(filename, mtimes):
        return False  # Simulate no changes

    reloader.check_file = check_file  # type: ignore

    run_reloader(reloader)

    assert not before.is_set()  # Ensure before trigger was not called
    assert not after.is_set()   # Ensure after trigger was not called

def test_reloader_triggers_multiple_changes(app: Sanic, app_loader: AppLoader):
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
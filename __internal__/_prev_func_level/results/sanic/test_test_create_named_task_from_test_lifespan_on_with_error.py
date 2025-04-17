import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
def test_stop_app_without_running_tasks():
    app = Sanic("TestApp")

    @app.before_server_start
    async def setup(app, _):
        pass

    @app.after_server_start
    async def stop(app, _):
        app.stop()

    app.run(single_process=True)

    assert not app._task_registry

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
def test_stop_app_with_running_tasks():
    app = Sanic("TestApp")

    async def dummy_task():
        await asyncio.sleep(1)

    @app.before_server_start
    async def setup(app, _):
        app.add_task(dummy_task, name="dummy_task")

    @app.after_server_start
    async def stop(app, _):
        task = app.get_task("dummy_task")
        assert app._task_registry
        assert isinstance(task, asyncio.Task)
        assert task.get_name() == "dummy_task"
        app.stop()

    app.run(single_process=True)

    assert not app._task_registry

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
def test_stop_app_with_nonexistent_task():
    app = Sanic("TestApp")

    @app.before_server_start
    async def setup(app, _):
        pass

    @app.after_server_start
    async def stop(app, _):
        with pytest.raises(SanicException):
            app.get_task("nonexistent_task")
        app.stop()

    app.run(single_process=True)
import asyncio
import pytest
from sanic import Sanic

@pytest.mark.skipif(sys.version_info < (3, 8), reason='Not supported in 3.7')
def test_stop_app(app, port):
    async def dummy(): 
        await asyncio.sleep(1)

    @app.before_server_start
    async def setup(app, _):
        app.add_task(dummy, name="dummy_task")

    @app.after_server_start
    async def after_start(app, _):
        task = app.get_task("dummy_task")
        assert app._task_registry
        assert isinstance(task, asyncio.Task)
        assert task.get_name() == "dummy_task"

        app.stop()

    app.run(single_process=True, port=port)

    # Verify that the app has stopped
    assert not app.is_running
    assert "dummy_task" not in app._task_registry

@pytest.mark.parametrize('task_name', ['non_existent_task', 'dummy_task'])
def test_stop_non_existent_task(app, port, task_name):
    async def dummy(): 
        await asyncio.sleep(1)

    @app.before_server_start
    async def setup(app, _):
        app.add_task(dummy, name="dummy_task")

    @app.after_server_start
    async def after_start(app, _):
        if task_name == 'non_existent_task':
            with pytest.raises(SanicException):
                app.get_task(task_name)
        else:
            task = app.get_task(task_name)
            assert isinstance(task, asyncio.Task)
            app.stop()

    app.run(single_process=True, port=port)
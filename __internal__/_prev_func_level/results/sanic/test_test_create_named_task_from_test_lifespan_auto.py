import asyncio
import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

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

    app.run(single_process=True, port=port)

    app.stop()

    with pytest.raises(SanicException, match='Registered task named "dummy_task" not found.'):
        app.get_task("dummy_task", raise_exception=True)

    assert not app._task_registry
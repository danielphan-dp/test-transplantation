import pytest
from sanic import Sanic
from sanic_testing import testing

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_empty_list(app, listener_name):
    """Test that the listener works with an empty list"""
    output = []
    app.listener(listener_name)(create_listener_no_loop(listener_name, output))
    start_stop_app(app)
    assert output == [app.name + listener_name]

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_multiple_calls(app, listener_name):
    """Test that multiple calls to the listener update the list correctly"""
    output = []
    app.listener(listener_name)(create_listener_no_loop(listener_name, output))
    start_stop_app(app)
    start_stop_app(app)  # Call it again to test multiple invocations
    assert output == [app.name + listener_name, app.name + listener_name]

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_different_app_names(app, listener_name):
    """Test that different app names are handled correctly"""
    app2 = Sanic("AnotherApp")
    output1 = []
    output2 = []
    app.listener(listener_name)(create_listener_no_loop(listener_name, output1))
    app2.listener(listener_name)(create_listener_no_loop(listener_name, output2))
    start_stop_app(app)
    start_stop_app(app2)
    assert output1 == [app.name + listener_name]
    assert output2 == [app2.name + listener_name]
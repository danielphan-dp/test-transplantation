import pytest

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_multiple_listeners_no_loop(app, listener_name):
    """Test that multiple listeners work correctly"""
    output = []
    # Register multiple listeners
    for name in AVAILABLE_LISTENERS:
        app.listener(name)(create_listener_no_loop(name, output))
    start_stop_app(app)
    for name in AVAILABLE_LISTENERS:
        assert app.name + name == output.pop()

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_with_empty_list(app, listener_name):
    """Test that listener works with an initially empty list"""
    output = []
    app.listener(listener_name)(create_listener_no_loop(listener_name, output))
    start_stop_app(app)
    assert app.name + listener_name == output.pop()

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_with_existing_data(app, listener_name):
    """Test that listener correctly prepends to an existing list"""
    output = [f'Existing data']
    app.listener(listener_name)(create_listener_no_loop(listener_name, output))
    start_stop_app(app)
    assert app.name + listener_name == output.pop(0)
    assert output == ['Existing data']  # Ensure existing data is preserved

@pytest.mark.parametrize('listener_name', AVAILABLE_LISTENERS)
def test_listener_no_loop_order(app, listener_name):
    """Test that listeners are called in the correct order"""
    output = []
    app.listener('first_listener')(create_listener_no_loop('first_listener', output))
    app.listener('second_listener')(create_listener_no_loop('second_listener', output))
    start_stop_app(app)
    assert output == [app.name + 'second_listener', app.name + 'first_listener']  # Check order of execution
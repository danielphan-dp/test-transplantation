import pytest
from unittest.mock import MagicMock
from uvicorn.config import Config
from uvicorn import LifespanOff

@pytest.mark.parametrize("closed_initial_state, expected_closed_state", [
    (False, True),
    (True, True)
])
def test_close_method(closed_initial_state, expected_closed_state):
    config = Config(app=MagicMock())
    lifespan = LifespanOff(config)
    lifespan.closed = closed_initial_state

    if closed_initial_state:
        with pytest.raises(AssertionError):
            lifespan.close()
    else:
        lifespan.close()
        assert lifespan.closed == expected_closed_state
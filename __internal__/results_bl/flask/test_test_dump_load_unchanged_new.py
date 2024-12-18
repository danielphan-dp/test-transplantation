import pytest
from datetime import datetime, timezone
from uuid import uuid4
from markupsafe import Markup
from flask.json.tag import JSONTag, TaggedJSONSerializer

@pytest.mark.parametrize('data', [
    {'t': (1, 2, 3)},
    {'t__': b'a'},
    {'di': 'di'},
    {'x': (1, 2, 3), 'y': 4},
    (1, 2, 3),
    [(1, 2, 3)],
    b'\xff',
    Markup('<html>'),
    uuid4(),
    datetime.now(tz=timezone.utc).replace(microsecond=0),
    None,
    '',
    {},
    {'key': None},
    {'key': {'nested_key': 'value'}}
])
def test_loads_edge_cases(data):
    s = TaggedJSONSerializer()
    if data is None:
        with pytest.raises(TypeError):
            s.loads(s.dumps(data))
    else:
        assert s.loads(s.dumps(data)) == data

def test_loads_with_custom_object_hook():
    def custom_hook(dct):
        return {k: v for k, v in dct.items() if k != 'exclude'}
    
    s = TaggedJSONSerializer()
    data = {'include': 1, 'exclude': 2}
    result = s.loads(s.dumps(data), object_hook=custom_hook)
    assert result == {'include': 1}
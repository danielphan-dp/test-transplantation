import glob
import os
import pytest
import treq
import types
import importlib.machinery

@pytest.mark.parametrize('fname', glob.glob('path/to/httpfiles/*.py'))
def test_load_py_valid(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    assert 'request' in env
    assert 'cfg' in env

@pytest.mark.parametrize('fname', glob.glob('path/to/httpfiles/*.py'))
def test_load_py_request_structure(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env['request']
    assert callable(expect)

@pytest.mark.parametrize('fname', glob.glob('path/to/httpfiles/*.py'))
def test_load_py_cfg_instance(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    cfg = env['cfg']
    assert isinstance(cfg, Config)

def test_load_py_invalid_file():
    with pytest.raises(FileNotFoundError):
        treq.load_py('invalid_file.py')

def test_load_py_empty_file():
    with open('empty_file.py', 'w') as f:
        pass
    env = treq.load_py('empty_file.py')
    assert 'request' not in env
    assert 'cfg' in env
    os.remove('empty_file.py')
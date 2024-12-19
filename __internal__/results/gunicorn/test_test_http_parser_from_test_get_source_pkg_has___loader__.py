import glob
import os
import pytest
import treq
import types
import importlib.machinery

dirname = os.path.dirname(__file__)
reqdir = os.path.join(dirname, "requests", "valid")
httpfiles = glob.glob(os.path.join(reqdir, "*.http"))

@pytest.mark.parametrize("fname", httpfiles)
def test_load_py_valid(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    assert 'request' in env
    assert 'cfg' in env

@pytest.mark.parametrize("fname", httpfiles)
def test_load_py_invalid_file():
    with pytest.raises(FileNotFoundError):
        treq.load_py("non_existent_file.py")

@pytest.mark.parametrize("fname", httpfiles)
def test_load_py_syntax_error(fname):
    with pytest.raises(SyntaxError):
        treq.load_py(os.path.join(reqdir, "invalid_syntax.py"))

@pytest.mark.parametrize("fname", httpfiles)
def test_load_py_edge_case(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env['request']
    cfg = env['cfg']
    req = treq.request(fname, expect)
    
    for case in req.gen_cases(cfg):
        assert callable(case[0])
        case[0](*case[1:])
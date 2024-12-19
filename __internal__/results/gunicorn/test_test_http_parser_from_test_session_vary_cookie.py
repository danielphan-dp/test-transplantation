import glob
import os
import pytest
import treq

@pytest.mark.parametrize('fname', glob.glob("httpfiles/*.http"))
def test_http_parser_invalid_method(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env["request"]
    cfg = env["cfg"]
    req = treq.badrequest(fname)

    with pytest.raises(expect):
        req.check(cfg)

@pytest.mark.parametrize('fname', glob.glob("httpfiles/*.http"))
def test_http_parser_missing_headers(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env["request"]
    cfg = env["cfg"]
    req = treq.badrequest(fname)

    with pytest.raises(expect):
        req.check(cfg)

@pytest.mark.parametrize('fname', glob.glob("httpfiles/*.http"))
def test_http_parser_invalid_uri(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env["request"]
    cfg = env["cfg"]
    req = treq.badrequest(fname)

    with pytest.raises(expect):
        req.check(cfg)

@pytest.mark.parametrize('fname', glob.glob("httpfiles/*.http"))
def test_http_parser_large_request(fname):
    env = treq.load_py(os.path.splitext(fname)[0] + ".py")
    expect = env["request"]
    cfg = env["cfg"]
    req = treq.badrequest(fname)

    with pytest.raises(expect):
        req.check(cfg)
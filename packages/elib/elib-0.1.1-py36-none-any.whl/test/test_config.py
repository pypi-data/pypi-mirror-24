# coding=utf-8

import os

import pytest

from elib.config import BaseConfig
from elib.config.property import ConfigProp


class DummyConfig(BaseConfig):

    @ConfigProp(False, bool)
    def debug(self):
        pass

    @ConfigProp('', str)
    def string(self):
        pass

    @ConfigProp(0, int)
    def integer(self):
        pass

    @ConfigProp(None, list)
    def some_list(self):
        pass

    @ConfigProp('', str, 'namespace')
    def key(self):
        pass


def test_create_config():
    cfg = DummyConfig('test')
    assert cfg.debug is False
    assert not cfg.string
    assert cfg.integer is 0


def test_ini_config_file():
    with open('test.ini', 'w') as stream:
        stream.write('''
[main]
debug=true
string=some string
integer=1
''')
    cfg = DummyConfig('test')
    assert cfg.debug is True
    assert cfg.string == 'some string'
    assert cfg.integer is 1


@pytest.mark.parametrize('ext', ['yaml', 'yml'])
def test_yaml_config_file(ext):
    with open(f'test.{ext}', 'w') as stream:
        stream.write('''
debug: "true"
string: some string
integer: 1
''')
    cfg = DummyConfig('test')
    assert cfg.debug is True
    assert cfg.string == 'some string'
    assert cfg.integer is 1


@pytest.mark.parametrize('key', ['debug', 'DEBUG'])
def test_default_dict(key):
    cfg = DummyConfig(
        'test', {key: 'true', 'string': 'some string', 'integer': 1})
    assert cfg.debug is True
    assert cfg.string == 'some string'
    assert cfg.integer is 1


@pytest.mark.parametrize('ext', ['yaml', 'yml'])
def test_yaml_lists(ext):
    with open(f'test.{ext}', 'w') as stream:
        stream.write('''
debug: "true"
string: some string
integer: 1
some_list:
  - caribou
  - pingu
  - moose
''')
    cfg = DummyConfig('test')
    assert cfg.some_list == ['caribou', 'pingu', 'moose']


@pytest.mark.parametrize('ext', ['yaml', 'yml'])
def test_yaml_namespace(ext):
    with open(f'test.{ext}', 'w') as stream:
        stream.write('''
debug: "true"
string: some string
integer: 1
some_list:
  - caribou
  - pingu
  - moose
namespace:
  key: value
''')
    cfg = DummyConfig('test')
    assert cfg.key == 'value'

# coding=utf-8
"""
Manages ESST configuration
"""

import collections
import os

import everett
import everett.manager
import yaml


def update_nested_dict(target_dict: collections.MutableMapping,
                       source_dict: collections.MutableMapping) -> collections.MutableMapping:
    for key, value in source_dict.items():
        if isinstance(value, collections.MutableMapping):
            target_dict[key.upper()] = update_nested_dict(target_dict.get(key, {}), value)
        else:
            target_dict[key.upper()] = source_dict[key]
    return target_dict


def flatten_dict(source_dict: collections.MutableMapping, parent_key='', sep='_') -> dict:
    items = []
    for key, value in source_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, collections.MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


class YAMLConfig:
    def __init__(self, possible_paths):
        self.cfg = {}
        possible_paths = everett.manager.listify(possible_paths)

        for path in possible_paths:
            if not path:
                continue

            path = os.path.abspath(os.path.expanduser(path.strip()))
            if path and os.path.isfile(path):
                self.cfg = update_nested_dict(
                    self.cfg, self.parse_yaml_file(path))

        self.cfg = flatten_dict(self.cfg)

    @staticmethod
    def parse_yaml_file(path: str):
        with open(path) as stream:
            return yaml.load(stream)

    def get(self, key, namespace=None):
        value = everett.manager.get_key_from_envs(self.cfg, key, namespace)
        if value is everett.NO_VALUE:
            return value
        else:
            if isinstance(value, bool):
                return str(value)
            return value

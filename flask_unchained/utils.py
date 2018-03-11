import datetime
import os
import re

from importlib import import_module

# alias these to the utils module
from .clips_pattern import de_camel, pluralize, singularize


class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __repr__(self):
        return f'AttrDict({super().__repr__()})'


def camel_case(string):
    if not string:
        return string
    parts = snake_case(string).split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


def class_case(string):
    return title_case(string).replace(' ', '')


def format_docstring(docstring):
    if not docstring:
        return ''
    return re.sub(r'\s+', ' ', docstring).strip()


def get_boolean_env(name, default):
    default = 'true' if default else 'false'
    return os.getenv(name, default).lower() in {'true', 'yes', 'y', '1'}


def kebab_case(string):
    if not string:
        return string
    string = string.replace('_', '-').replace(' ', '-')
    return de_camel(string, '-').strip('-')


def right_replace(string, old, new, count=1):
    if not string:
        return string
    return new.join(string.rsplit(old, count))


def safe_import_module(module_name):
    """
    Like importlib's import_module, except it does not raise ImportError
    if the requested module_name was not found
    """
    try:
        return import_module(module_name)
    except ImportError as e:
        if module_name not in str(e):
            raise e


def snake_case(string):
    if not string:
        return string
    string = string.replace('-', '_').replace(' ', '_')
    return de_camel(string)


def title_case(string):
    if not string:
        return string
    string = string.replace('_', ' ').replace('-', ' ')
    return de_camel(string, ' ').title().strip()


def utcnow():
    """
    Returns a current timezone-aware datetime.datetime in UTC
    """
    return datetime.datetime.now(datetime.timezone.utc)

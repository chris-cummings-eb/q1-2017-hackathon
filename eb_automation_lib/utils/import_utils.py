import importlib.util
from inspect import getargspec
import os
import re


def get_module_from_filepath(filepath):
    _, module_name = os.path.split(filepath)
    module_name = module_name.replace('.py', '')

    spec = importlib.util.spec_from_file_location(module_name, location=filepath)
    module = importlib.util.module_from_spec(spec)

    def module_reference(spec, module):
            spec.loader.exec_module(module)
            return module

    return lambda: module_reference(spec, module)


def docstring(python_object):
    return python_object.__doc__ or ''


def display_name(python_object):
    match = re.search(
        r'(?<=##NAME:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0).strip() if match else python_object.__name__


def icon_type(python_object):
    match = re.search(
        r'(?<=##ICON:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0).strip() if match else ''


def tag_type(python_object):
    match = re.search(
        r'(?<=##TAGS:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0).strip().replace(',', '').split(' ') if match else []


def get_args(python_object):
    if callable(python_object):
        return getargspec(python_object).args
    return []


def description(python_object):
    match = re.search(
        r'(?<=##DESCRIPTION:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0).strip() if match else docstring(python_object)

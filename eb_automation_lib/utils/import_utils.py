import importlib.util
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
    match = re.match(
        r'(?<=##NAME:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0) if match else python_object.__name__


def icon_type(python_object):
    match = re.match(
        r'(?<=##TYPE:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0) if match else docstring(python_object)


def description(python_object):
    match = re.match(
        r'(?<=##DESCRIPTION:).+$',
        docstring(python_object),
        flags=re.MULTILINE
    )

    return match.group(0) if match else docstring(python_object)

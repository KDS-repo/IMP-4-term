import re
import inspect
import types


def is_function(obj) -> bool:
    return (
        is_method(obj)
        or inspect.isfunction(obj)
        or isinstance(obj, types.MethodWrapperType)
    )


def is_primitive(obj) -> bool:
    return (
        isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, bool)
        or isinstance(obj, str)
        or isinstance(obj, type(None))
    )


def is_map(obj) -> bool:
    return isinstance(obj, dict) or isinstance(obj, types.MappingProxyType)


def is_list(obj) -> bool:
    return isinstance(obj, list) or isinstance(obj, tuple)


def is_method(obj) -> bool:
    return inspect.ismethod(obj) or isinstance(obj, staticmethod)


def is_custom(obj) -> bool:
    return True


def is_none(obj) -> bool:
    return obj is None


def is_magicmarked(obj) -> bool:
    return re.match("^__(?:\w+)__$", obj) != None


def is_code(obj) -> bool:
    return inspect.iscode(obj)

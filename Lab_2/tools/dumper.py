from .inspector import (
    is_function,
    is_none,
    is_map,
    is_list,
    is_custom,
    is_primitive,
    is_method,
    is_code,
)
import builtins


def get_dump_obj(obj):
    for isthis, dump in dump_type:
        if isthis(obj):
            return dump(obj)


def dump_attr(obj):
    res = {}
    for attr in dir(obj):
        if not attr.startswith("__"):
            attr_value = getattr(obj, attr)
            res[attr] = get_dump_obj(attr_value)
    return res


def dump_code(obj):
    return {
        ".code": {
            "co_argcount": obj.co_argcount,
            "co_code": list(obj.co_code),
            "co_cellvars": obj.co_cellvars,
            "co_consts": get_dump_obj(obj.co_consts),
            "co_filename": obj.co_filename,
            "co_firstlineno": obj.co_firstlineno,
            "co_flags": obj.co_flags,
            "co_lnotab": list(obj.co_lnotab),
            "co_freevars": obj.co_freevars,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_name": obj.co_name,
            "co_names": obj.co_names,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_varnames": obj.co_varnames,
        }
    }


def dump_primitive(obj):
    return obj


def dump_list(objs):
    return [get_dump_obj(obj) for obj in objs]


def dump_dict(objs):
    return {
        get_dump_obj(key): get_dump_obj(value) for key, value in objs.items()
    }


def dump_class(obj):
    try:
        result = {"__name__": obj.__name__, "__attr__": dump_attr(obj)}
    except AttributeError:
        result = {"__class__": str(obj.__class__), "__attr__": dump_attr(obj)}
    return {".castom_class": result}


def get_global_vars(func):
    gls = {}
    for global_var in func.__code__.co_names:
        if global_var in func.__globals__:
            if "module" in str(func.__globals__[global_var]):
                gls[global_var] = str(func.__globals__[global_var])
            else:
                gls[global_var] = get_dump_obj(func.__globals__[global_var])
    return gls


def dump_func(obj):
    if is_method(obj):
        obj = obj.__func__
    code = dump_code(obj.__code__)
    gls = get_global_vars(obj)
    closure = None
    return {
        ".castom_func": {
            "__code__": code,
            "__globals__": gls,
            "__name__": obj.__name__,
            "__closure__": closure,
        }
    }


dump_proceeded = list()


def dump_custom(obj):
    if id(obj) not in dump_proceeded:
        #dump_proceeded.append(id(obj))
        if is_code(obj):
            return dump_code(obj)
        if is_function(obj):
            return dump_func(obj)
        else:
            return dump_class(obj)
    else:
        pass


dump_type = [
    # primitive
    (lambda obj: (is_primitive(obj) == True), dump_primitive),
    # container
    (lambda obj: (is_map(obj) == True), dump_dict),
    (lambda obj: (is_list(obj) == True), dump_list),
    # custom
    (lambda obj: (is_custom(obj) == True), dump_custom),
]

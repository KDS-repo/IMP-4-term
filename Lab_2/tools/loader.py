import types
import builtins
from .inspector import is_none, is_function, is_list, is_map, is_code
import types


def get_load_obj(obj):
    if is_code(obj):
        return load_code(obj)
    elif is_map(obj):
        for (key, value) in obj.items():
            if type(key) == str and key.startswith("."):
                return load_types[key](value)
            else:
                return load_dict(obj)
    else:
        return load_types[type(obj)](obj)


def load_primitive(obj):
    return obj


def load_list(obj):
    res = []
    for value in obj:
        res.append(get_load_obj(value))
    return res


def load_dict(obj):
    res = {}
    for key, value in obj.items():
        res[get_load_obj(key)] = get_load_obj(value)
    return res


def load_module(obj):
    return __import__(obj)


def load_func(obj):
    arguments = obj["__code__"][".code"]
    gls = obj["__globals__"]
    gls["__builtins__"] = builtins
    for key in obj["__globals__"]:
        if key in arguments["co_names"]:
            m = obj["__globals__"][key]
            if type(m) is str:
                if "module" in m:
                    gls[key] = load_module(str(m).split("'")[1])
            else:
                gls[key] = get_load_obj(m)
    return types.FunctionType(load_code(arguments), gls)

def load_class(obj):
    vars = {}
    for attr, value in obj["__attr__"].items():
        if attr != '__name__':
            vars[attr] = get_load_obj(value)
    try:
        return type(obj["__name__"], (), vars)
    except KeyError:
        return type(obj["__class__"], (), vars)


def load_code(obj):
    return types.CodeType(
        obj["co_argcount"],
        obj["co_posonlyargcount"],
        obj["co_kwonlyargcount"],
        obj["co_nlocals"],
        obj["co_stacksize"],
        obj["co_flags"],
        bytes(obj["co_code"]),
        tuple(get_load_obj(obj["co_consts"])),
        tuple(obj["co_names"]),
        tuple(obj["co_varnames"]),
        obj["co_filename"],
        obj["co_name"],
        obj["co_firstlineno"],
        bytes(obj["co_lnotab"]),
        tuple(obj["co_freevars"]),
        tuple(obj["co_cellvars"]),
    )

load_types = {
    type(None): load_primitive,
    int: load_primitive,
    float: load_primitive,
    bool: load_primitive,
    str: load_primitive,
    dict: load_dict,
    list: load_list,
    tuple: load_list,
    ".castom_func": load_func,
    ".castom_class": load_class,
    ".code": load_code,
}

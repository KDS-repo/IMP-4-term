
#-------------------------------------------------------------
#tools packager

def pack(obj):
    return get_dump_obj(obj)


def unpack(obj):
    return get_load_obj(obj)

#----------------------------------------------------------------------------
#yaml parser
from yaml import load, dump


class YamlParser:
    def dumps(self, obj):
        p = pack(obj)
        return dump(p, indent = 4)

    def dump(self, obj, fp):
        return fp.write(self.dumps(obj))

    def loads(self, s):
        l = load(s)
        return unpack(l)

    def load(self, fp):
        return self.loads(fp.read())

    def unpack(self, fp):
        return load(fp.read())

    def pack(self, obj, fp):
        return fp.write(dump(obj))

#----------------------------------------------------------------------------
#tools inspector
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

#---------------------------------------------------------------
#tools dumper
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

#----------------------------------------------------------------
#tools loader
import types
import builtins


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
#---------------------------------------------------------------------------------------
#json encoder
class JsonEncoder:
    def __init__(self, tab="\t", crlf="\n"):
        self.nesting_level = 0
        self.tab = tab
        self.crlf = crlf
        self.joiner = "," + self.crlf

    def add_tab(self, level=-1):
        if level != -1:
            self.nesting_level = level
        return self.nesting_level * self.tab

    def dict_to_json(self, objs):
        bracket = self.json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.nesting_level += 1
        return (
            bracket[0]
            + self.crlf
            + self.joiner.join(
                [
                    str(
                        self.add_tab()
                        + self.json_encode(key)
                        + ": "
                        + self.json_encode(value)
                    )
                    for key, value in objs.items()
                ]
            )
            + self.crlf
            + self.add_tab(self.nesting_level - 1)
            + bracket[1]
        )

    def array_to_json(self, objs):
        bracket = self.json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.nesting_level += 1
        return (
            bracket[0]
            + self.crlf
            + self.joiner.join(
                [str(self.add_tab() + self.json_encode(obj)) for obj in objs]
            )
            + self.crlf
            + self.add_tab(self.nesting_level - 1)
            + bracket[1]
        )

    def primitive_to_json(self, obj):
        return str(obj)

    def bool_to_json(self, obj):
        return str(obj).lower()

    def none_to_json(self, obj):
        return "null"

    def string_to_json(self, obj):
        bracket = self.json_brackets[type(obj)]
        return bracket[0] + str(obj) + bracket[1]

    def json_encode(self, obj):
        if type(obj) in self.json_type:
            return self.json_type[type(obj)](self, obj)
        else:
            raise ValueError("can't encode: ", type(obj))

    json_brackets = {
        dict: ("{", "}"),
        list: ("[", "]"),
        tuple: ("[", "]"),
        str: ('"', '"'),
    }

    json_type = {
        int: primitive_to_json,
        float: primitive_to_json,
        str: string_to_json,
        bool: bool_to_json,
        dict: dict_to_json,
        list: array_to_json,
        tuple: array_to_json,
        type(None): none_to_json,
    }
    
#---------------------------------___--------------------------------------
#json decoder
class JsonDecoder:
    def __init__(self):
        self.json_to_true = self.json_to_castom("true", True)
        self.json_to_false = self.json_to_castom("false", False)
        self.json_to_none = self.json_to_castom("null", None)

        self.json_types = [
            ("{", self.json_to_dict),
            ("[", self.json_to_list),
            ('"', self.json_to_string),
            (self.int_const, self.json_to_numberic),
            ("false", self.json_to_false),
            ("true", self.json_to_true),
            ("null", self.json_to_none),
        ]

    def json_to_castom(self, word, value=None):
        def result(obj):
            if obj.startswith(word):
                return value, obj[len(word) :]

        result.__name__ = "parse_%s" % word
        return result

    def json_to_dict(self, objs):
        res = {}
        objs = remove_prefix(objs, "{").lstrip()
        while not objs.startswith("}"):
            (key, objs) = self.json_to_obj(objs)
            objs = remove_prefix(objs, ":")
            (value, objs) = self.json_to_obj(objs)
            res[key] = value
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "}")

    def json_to_list(self, objs):
        res = []
        objs = remove_prefix(objs, "[").lstrip()
        while not objs.startswith("]"):
            (value, objs) = self.json_to_obj(objs)
            res.append(value)
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "]")

    def json_to_numberic(self, obj):
        for i in range(len(obj)):
            if obj[i] not in self.int_const and obj[i] != ".":
                try:
                    return int(obj[:i]), obj[i:]
                except ValueError:
                    return float(obj[:i]), obj[i:]

        return

    def json_to_string(self, obj):
        obj = remove_prefix(obj, '"')
        tmp = obj.find('"')
        return obj[:tmp], obj[tmp + 1 :]

    def json_to_obj(self, obj):
        obj = obj.lstrip()
        for (char, func) in self.json_types:
            if not obj:
                pass
            elif obj.startswith(char):
                return func(obj)

        raise ValueError("can't decode: " + obj.split(","))

    def json_decode(self, obj):
        (item, obj) = self.json_to_obj(obj)
        obj = obj.lstrip()
        if obj != "":
            raise ValueError("bad format")
        else:
            return item

    int_const = tuple("1 2 3 4 5 6 7 8 9 0".split(" "))


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text
#---------------------------------------------------------------------------
#libs json __init__

def dumps(obj):
    return JsonEncoder().json_encode(obj)


def loads(obj):
    return JsonDecoder().json_decode(obj)
#-------------------------------------------------------------------------
#libs json jsonparcer


class JsonParser:
    def dumps(self, obj):
        p = pack(obj)
        return dumps(p)
    
    def dump(self, obj, fp):
        return fp.write(self.dumps(obj))
    
    def loads(self, s):
        l = loads(s)
        return unpack(l)
    
    def load(self, fp):
        return self.loads(fp.read())
    
    def unpack(self, fp):
        return loads(fp.read())
    
    def pack(self, obj, fp):
        return fp.write(dumps(obj))
#-----------------------------------------------------------------------
#factory
    
class Serializator:
    def __init__(self):
        self.parsers = dict()
    
    def add_parser(self, format, parser):
        self.parsers[format.lower()] = parser
    
    def get_parser(self, format):
        parser = self.parsers.get(format.lower())
        if not parser:
            raise ValueError(format)
        return parser()


serializer = Serializator()
serializer.add_parser("JSON", JsonParser)
serializer.add_parser("Yaml", YamlParser)

#-------------------------------------------------------------
#dump

types = {
    "yaml": serializer.get_parser("yaml"),
    "json": serializer.get_parser("json"),
}

def dump(in_file, out_file):
    ifile = open(in_file, "r")
    ofile = open(out_file, "w")
    obj = types[in_file.split(".")[-1].lower()].unpack(ifile)
    types[out_file.split(".")[-1].lower()].pack(obj, ofile)
    ifile.close()
    ofile.close()
    

#---------------------------------------------------------------------
#command_line
import argparse

def main():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("in_file", type=str, help="Input file for pars")
    parser.add_argument("out_file", type=str, help="Output file to load")
    args = parser.parse_args()
    
    dump(args.in_file, args.out_file)


if __name__ == "__main__":
    main()
#----------------------------------------------------------------
def deserialise(filename):
    out_code = types.CodeType(
        co_argcount,
        co_posonlyargcount,
        co_kwonlyargcount,
        co_nlocals,
        co_stacksize,
        co_flags,
        co_code,
        co_consts,
        co_names,
        co_varnames,
        co_filename,
        name,
        co_firstlineno,
        co_lnotab,
        co_freevars,
        co_cellvars)
    return types.FunctionType(out_code, glob, name)
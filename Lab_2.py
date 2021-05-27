import pickle
import types
import json
import marshal

def create_function(name, args):
    def y(): pass
    print(dir(y))
    print(dir(y.__code__))
    print(y.__code__.__dir__())
    y_code = types.CodeType(y.__code__.co_argcount,
                y.__code__.co_nlocals,
                y.__code__.co_stacksize,
                y.__code__.co_flags,
                y.__code__.co_code,
                y.__code__.co_consts,
                y.__code__.co_names,
                y.__code__.co_varnames,
                y.__code__.co_freevars,
                y.__code__.co_cellvars,
                y.__code__.co_filename,
                name,
                y.__code__.co_firstlineno,
                y.__code__.co_lnotab)
    return types.FunctionType(y_code, y.__globals__, name)

class Attempt(object):
    def func():
        print("Hello")
    field = 45
    field2 = 4

def main():
    a = create_function("attempt", ())
    a()
    
if __name__ == "__main__":
    main()

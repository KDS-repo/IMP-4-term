import pickle
import types

class Attempt(object):
    def func():
        print("Hello")
    field = 45
    field2 = 4
 
def create_function(name, args):
    def y(): pass
    y_code = types.CodeType(args,
                y.func_code.co_nlocals,
                y.func_code.co_stacksize,
                y.func_code.co_flags,
                y.func_code.co_code,
                y.func_code.co_consts,
                y.func_code.co_names,
                y.func_code.co_varnames,
                y.func_code.co_filename,
                name,
                y.func_code.co_firstlineno,
                y.func_code.co_lnotab)
    return types.FunctionType(y_code, y.func_globals, name)

def main():
#    attempt = 35
#    output = pickle.dumps(attempt)
#    print(attempt)
#    print(output)
    a = Attempt()
    #creating instance field that covers class attribute
    a.field = 55
    print(Attempt.field)
    print(a.field)
    #a little mixup to be remembered, the funcname is has ATTR, but looks for fields too
    print(hasattr(a, "field"))
    #deleting instance field, revealing class attribute
    del a.field
    print(Attempt.field)
    print(Attempt.__dict__)
    print(a.field)
    print(hasattr(a, "field"))
    
    print(dir(Attempt.func))
    for part in dir(Attempt.func):
        print(part)
        print(hasattr(Attempt.func, part))
        if(hasattr(Attempt.func, part)):
            print(getattr(Attempt.func, part))
            
    f_dict = dir(Attempt.func)
    a = create_function("FuncName", f_dict)
    
    
    
if __name__ == "__main__":
    main()

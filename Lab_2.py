import pickle
import types
 
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

class Attempt(object):
    def func():
        print("Hello")
    field = 45
    field2 = 4

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
    print(Attempt.func)
    print(Attempt.__dict__)
    print(a.field)
    print(hasattr(a, "field"))
    
    exec(Attempt.func.__code__)
    
    def newfunc():
        pass
    
    #newfunc = type(Attempt.func.__name__, (), Attempt.func.__dict__)
    #newfunc()
    #type(...) doesn't work like that, if it did, it would print
    #proof - b = newfunc later
    print(type(Attempt.func))
    print(dir(Attempt.func))
    a = getattr(Attempt.func, "__code__")
    print("code\n", a)
    setattr(newfunc, "__code__", a)
    #for part in dir(Attempt.func):
        #print(part)
        #print(hasattr(Attempt.func, part))
        #if(hasattr(Attempt.func, part)):
            #a = getattr(Attempt.func, part)
            #print(a)
            #setattr(newfunc, part, a)
        
    print(newfunc)
    newfunc()
    b = newfunc
    b()
    
    #f_dict = dir(Attempt.func)
    #a = create_function("FuncName", f_dict)
    
    
    
if __name__ == "__main__":
    main()

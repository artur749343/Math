import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
OPERATORS={"+":lambda x, y: x+y, "-":lambda x, y: x-y, "*":lambda x, y: x*y, "/":lambda x, y: x/y, "**":lambda x, y: x**y}
LIST_LIMIT=256
Natural=(0, float("inf"), 1, False)
Integer=(float("-inf"), float("inf"), 1, False)
Real=(float("-inf"), float("inf"), 0, False)
Complex=(float("-inf"), float("inf"), 0, True)

def compile_text(func=None):
    if func==None:
        return []
    i, res=0, []
    while i<len((func)):
        c=""
        while i<len((func)) and type(func[i])==str and func[i] in "0123456789.":
            c+=func[i]
            i+=1
        if c.isdigit():
            res.append(int(c))
        elif c.replace(".", "").isdigit():
            res.append(float(c))
        
        if i<len(func) and func[i-1]==func[i]=="*":
            del res[-1]
            res.append("**")
        elif i<len(func) and func[i]=="^":
            res.append("**")
        elif i<len(func) and func[i]=="(":
            i+=1
            while func[i]!=")":
                c+=func[i]
                i+=1
            res.append(compile_text(c))
        elif i<len(func):
            res.append(func[i])
        if len(res)>1 and type(res[-2])==int and res[-1] not in list("+-*/")+["**"]:
            res.insert(-1, "*")
        i+=1
    return res

def get(self, *args, edit:bool=False, **kwargs):
    if type(type(self.func[0]))==type(type(self)):
        return [calculate(self, f.func, [args, kwargs]) for f in self.func if type(type(f))==type(type(self))]
    if len(args)>0 and type(args[0])==dict:
        kwargs, args=args[0], ()
    if edit:
        calculate(self, self.func, [args, kwargs])
    else:
        return calculate(self, deepcopy(self.func), [args, kwargs])

def calculate(self, func, args):
    if type(func)!=list:
        return func
    i, args, arg_cash=0, args[0], args[1]
    for n in [i for i in range(len(func)) if (type(func[i])==str and func[i] not in OPERATORS) or type(func[i])==list]:
        if type(func[n])==list:
            func[n]=calculate(self, func[n], [args[i:], arg_cash])
        elif func[n] in arg_cash:
            func[n]=arg_cash[func[n]]
        elif i<len(args):
            arg_cash.update({func[n]: args[i]})
            func[n]=args[i]
            i+=1
    for k, v in self.type.items():
        if k in arg_cash:
            if arg_cash[k]<v[0]: raise TypeError(f"argument less than {v[0]} in function {self}")
            if arg_cash[k]>v[1]: raise TypeError(f"argument more than {v[1]} in function {self}")
            if v[2]>0 and (arg_cash[k]*(v[2]**-1)%1): raise TypeError(f"argument is not correct: minimum step is {v[2]} in function {self}")
        
    if True in [((type(f)==str and f not in OPERATORS) or type(f)==list) for f in func]:
        return func
    else:
        arg, func=func[0], func[1:]
        for o, n in zip(func[::2], func[1::2]):
            arg=OPERATORS[o](arg, n)
        return arg
    

def show(self, start=0, stop=10):
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    x=list(to_list(self, max=100))
    ax.plot(np.linspace(-10, 10, len(x)), x, label=f'y=f(x)')
    ax.set_xlabel("x")
    ax.set_ylabel('y')
    ax.set_title("Function")
    ax.legend()
    plt.show()

def to_list(self, start=None, stop=None, step=None, max=LIST_LIMIT):
    start, stop, step=-max**(1/2) if start==None else start, max**(1/2) if stop==None else stop, max**(-1/2)*2 if step==None else step
    for k, v in self.type.items():
        if k in self.func:
            start=v[0] if start<v[0] else start
            stop=v[1] if stop>v[1] else stop
            step=v[2] if step<v[2] else step
    if step==0 or int((stop-start)/step)-1>LIST_LIMIT: raise TypeError(f"list biggest than {LIST_LIMIT}")
    l=np.linspace(start, stop, int((stop-start)/step)+1)
    for l1 in l:
        c=calculate(self, deepcopy(self.func), [[l1], {}])
        if type(c)!=list:
            yield c
        else:
            yield np.array(list(type(self)(c, self.type)), dtype=float)

def __add__(self, num):
    if type(type(self.func[0]))==type(type(self)):
        for f, f1 in zip(self.func, num.func):
            f.func+=["+", f1.func] if type(f1)==type(f) else ["+", f1]
    else:
        self.func+=["+", num.func] if type(num)==type(self) else ["+", num]
    return self
def __sub__(self, num):
    if type(type(self.func[0]))==type(type(self)):
        for f, f1 in zip(self.func, num.func):
            f.func+=["-", f1.func] if type(f1)==type(f) else ["-", f1]
    else:
        self.func+=["-", num.func] if type(num)==type(self) else ["-", num]
    return self
def __mul__(self, num):
    if type(type(self.func[0]))==type(type(self)):
        for f, f1 in zip(self.func, num.func):
            f.func+=["*", f1.func] if type(f1)==type(f) else ["*", f1]
    else:
        self.func+=["*", num.func] if type(num)==type(self) else ["*", num]
    return self
def __truediv__(self, num):
    if type(type(self.func[0]))==type(type(self)):
        for f, f1 in zip(self.func, num.func):
            f.func+=["/", f1.func] if type(f1)==type(f) else ["/", f1]
    else:
        self.func+=["/", num.func] if type(num)==type(self) else ["/", num]
    return self
def __pow__(self, num):
    if type(type(self.func[0]))==type(type(self)):
        for f, f1 in zip(self.func, num.func):
            f.func+=["**", f1.func] if type(f1)==type(f) else ["**", f1]
    else:
        self.func+=["**", num.func] if type(num)==type(self) else ["**", num]
    return self
def __neg__(self):
    self.func+=["*", -1]
    return self



def calc_str(_list):
    res=""
    for i in _list:
        if type(i)==list:
            res+="("+str(calc_str(i))+")"
        else:
            res+=str(i)
    return res

def to_str(self):
    if type(type(self.func[0]))==type(type(self)):
        res="("+str([f.__str__() for f in self.func if type(type(f))==type(type(self))]).replace("'", "")[1:-1]+")"
    else:
        res=calc_str(self.func)
    if type(self.get())!=list:
        return str(self.get())
    for k, v in self.type.items():
        res+="\n"+(str(v[0])+'<=' if v[0]!=float('-inf') else '')+(k)+('<='+str(v[1]) if v[1]!=float('inf') else '')+(' step='+str(v[2]) if v[2]!=0 else '')+(' complex' if v[3] else ' real')
    return res

class MathObject(type):
    def __new__(self, name, bases, namespace):
        for o, n, func in [("+", "__add__", __add__), ("-", "__sub__", __sub__), ("*", "__mul__", __mul__), ("/", "__truediv__", __truediv__), ("**", "__pow__", __pow__)]:
            if n in namespace:
                x=namespace[n]()
                namespace[n]=lambda x1, x2, o=o: x[1](x1.func+[o, x2.func]) if type(x2)==x[0] else func(x1, x2)
            else:
                namespace[n]=func
        if "__iter__" in namespace:
            namespace["iter"]=namespace["__iter__"]()
        namespace.update({"get": get, "show": show, "__iter__": to_list, "to_list": to_list, "__neg__": __neg__})
        if not "__str__" in namespace:
            namespace["__str__"]=to_str
        else:
            n=namespace["__str__"]
            namespace["__str__"]=lambda x: n(x, to_str(x))
        return super().__new__(self, name, bases, namespace)
    
    def __call__(self, func=None, arg=None, **kwargs):
        new_instance = super(MathObject, self).__call__()
        new_instance.type=kwargs if arg==None else arg
        new_instance.func=func if type(func)==list else compile_text(func) if type(func)==str else [func]
        if hasattr(new_instance, "__arg__"):
            func=new_instance.get(new_instance.__arg__())
            new_instance.func=func if type(func)==list else compile_text(func) if type(func)==str else [func]
        if hasattr(new_instance, "iter"):
            new_instance.func=[new_instance.iter[0](f) for f in func[:new_instance.iter[1]]]
        return new_instance


class Num(metaclass=MathObject):
    pass

def summa(d:int, u:int, n:Num):
    res=0
    for x in range(d, u+1):
        res+=n.get(x)
    return res

def prod(d:int, u:int, n:Num):
    res=1
    for x in range(d, u+1):
        res*=n.get(x)
    return res

def factorial(n):
    res=1
    for x in range(2, n+1):
        res*=x
    return res

def absolute(n):
    return -n if n<0 else n

def approxequal(num, epsilon):
    return num//epsilon*epsilon


def period(a:int, b:int):
    cash=[]
    while a!=0:
        a*=10
        cash.append(a//b)
        if cash[int(len(cash)/2):]==cash[:int(len(cash)/2)]:
            break
        a%=b
    cash[int(len(cash)/2):]

class Time(metaclass=MathObject):
    def __str__(self, x) -> str:
        if x.replace(".", "").isdigit():
            x=float(x)
            if x<3600 and 60<x:
                return str(x//60)+"m "+str(x%60)+"s"
            elif x<86400 and 3600<x:
                return str(x//3600)+"h "+str(x%3600//60)+"m "+str(x%60)+"s"
            elif 86400<x:
                return str(x//86400)+"d "+str(x%86400//3600)+"h "+str(x%3600//60)+"m "+str(x%60)+"s"
            return str(x)+"s"
        else:
            return x+"s"
    def __arg__(self):
        return {"s": 1, "m": 60, "h": 3600}

class Speed(metaclass=MathObject):
    def __str__(self, x) -> str:
            return x+"m/s"

class Metr(metaclass=MathObject):
    def __str__(self, x) -> str:
        if x.replace(".", "").isdigit():
            x=float(x)
            if x<1 and 0.1<x:
                return str(x*10)+"dm"
            elif x<0.1 and 0.01<x:
                return str(x*100)+"cm"
            elif x<0.01 and 0.001<x:
                return str(x*1000)+"mm"
            return str(x)+"m"
        else:
            return x+"m"
    def __truediv__():
        return Time, Speed

class Vector3(metaclass=MathObject):
    def __iter__():
        return Metr, 3
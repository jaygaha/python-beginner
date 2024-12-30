# Variable scope: where a variable is visible and accessible
# scope resolution = (LEGB) Local -> Enclosed -> Global -> Built In

# Local

def func1():
    a = 1
    print(a)

def func2():
    b = 2
    print(b)

func1()
func2()

# Enclosed

def e_func1():
    x = 1
    def func2():
        print(x)

    func2()

e_func1()


# Global

def g_func1():
    print(g)

def g_func2():
    print(g)

g = 4
g_func1()
g_func2()

# Built-in
from math import e

def b_func1():
    print(e)

b_func1()

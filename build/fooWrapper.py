from ctypes import cdll
lib = cdll.LoadLibrary('./libFoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self):
        lib.Foo_bar(self.obj)
    def fault(self):
        lib.Foo_fault(self.obj)
    def raise_fault(self, dummy):
        lib.Foo_raise_fault(self.obj)

def raise_a_fault(dummy):
    try:
        return lib.raise_a_fault(dummy)
    except Exception as inst:
        print "The fault is " + str(inst)          

from multiprocessing import Pool
import signal
import os

def sig_handler(signum, frame):
    print "segfault"
    raise Exception
    return None
signal.signal(signal.SIGSEGV, sig_handler)
os.kill(os.getpid(), signal.SIGSEGV)

# p = Pool(1)
# f = Foo()
# f.bar() #and you will see "Hello" on the screens
# f.fault() #this should cause a segmentation fault and the function will not return
items = [1, 2, 3, 4, 5]
try:
# results = p.map(raise_a_fault, items)

    results = raise_a_fault(5) #this should cause a segmentation fault and the function will not return
except Exception as inst:
    print "The exception is " + str(inst)

print "Results: " + str(results)
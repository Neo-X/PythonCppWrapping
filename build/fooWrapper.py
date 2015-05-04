from ctypes import cdll
lib = cdll.LoadLibrary('./libFoo.so')
import ctypes

class Foo(object):
    def __init__(self):
        self.obj = lib.Foo_new()

    def bar(self):
        lib.Foo_bar(self.obj)
    def fault(self):
        lib.Foo_fault(self.obj)
    def raise_fault(self, dummy):
        lib.Foo_raise_fault(self.obj)

def print_results(result):
    print "callback result: ***************** " + str (result)
    
def init_worker():
	# signal.signal(signal.SIGSEGV, sig_handler)
	# signal.signal(signal.SIGTERM, sig_handler)
	# signal.signal(signal.SIGINT, sig_handler)
	# signal.signal(signal.SIGINT, signal.SIG_IGN)
	# signal.signal(signal.SIGSEGV, signal.SIG_IGN)
	print ""

    
def raise_a_fault(dummy):
    # signal.signal(signal.SIGSEGV, sig_handler)
    # signal.signal(signal.SIGINT, signal.SIG_IGN)
    # os.kill(os.getpid(), signal.SIGSEGV)# This somehow triggers the signal properly
    print "raise_a_fault, pid " + str(os.getpid())
    try:
    	out = lib.raise_a_fault(dummy)
    except Exception as inst:
        print "The fault raised is " + str(inst)
        return None
        # ctypes.set_errno(-2)
    if out is None:
    	raise Exception('Runtime fault')
    print "Done causing error: " + str(out)
    return out
                  

from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import signal
import os


def sig_handler(signum, frame):
    print "segfault"
    # time.Sleep(0.001)
    print "sig_handler, pid " + str(os.getpid())
    print "sig_handler, ppid " + str(os.getppid())
    print "frame: " + str(frame)
    print(
        "Execution inside '{0}', "
        "with local namespace: {1}"
        .format(frame.f_code.co_name, frame.f_locals.keys()))
    # os.kill(os.getpid(), signal.SIGSEGV)# This somehow triggers the signal properly
    # ise Exception
    # ctypes.set_errno(-11)
    return None
# os.kill(os.getpid(), signal.SIGSEGV)# This somehow triggers the signal properly
# signal.signal(signal.SIGINT, signal.SIG_IGN)
# signal.signal(signal.SIGSEGV, signal.SIG_IGN)
# signal.signal(signal.SIGSEGV, sig_handler)
# signal.signal(signal.SIGTERM, sig_handler)
# signal.signal(signal.SIGINT, sig_handler)


processes_pool = Pool(2, init_worker)
# processes_pool = ThreadPool(2)
# init_worker()
print "main, pid " + str(os.getpid())
# f = Foo()
# f.bar() #and you will see "Hello" on the screens
# f.fault() #this should cause a segmentation fault and the function will not return
items = [1, 2, 3, 4, 5, 4, 3, 2, 1, 10, 2]
"""
try:
	# results = processes_pool.map(raise_a_fault, items).get(timeout=1)
	results = processes_pool.map(raise_a_fault, items)
except Exception as inst:
    print "The exception is " + str(inst)
print results
"""

try:
    for item in items:
        # this ensures the results come out in the same order the the experiemtns are in this list.
        try:
            result = processes_pool.apply_async(raise_a_fault, args = (item, ), callback = print_results)
            # results = raise_a_fault(item)
            result.get(timeout=2)
            # result.get()
        except Exception as inst:
            print "The exception is " + str(inst)
            continue
    # processes_pool.close()
    processes_pool.join()
    
except Exception as inst:
    print "The Out exception is " + str(inst)

    # results = raise_a_fault(5) #this should cause a segmentation fault and the function will not return

# print "Results: " + str(results)
print "All Done!"

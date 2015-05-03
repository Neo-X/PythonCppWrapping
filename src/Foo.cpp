
#include "../include/Foo.h"

extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo){ foo->bar(); }
    void Foo_fault(Foo* foo){ foo->fault(); }
    void Foo_raise_fault(Foo * foo) { foo->raise_fault(); }

    int raise_a_fault(int r)
	{
    	std::cout << "r is "<< r << std::endl;
    	if (r > 4)
    	{
    		volatile int *p = reinterpret_cast<volatile int*>(0);
			*p = 0x1337D00D;
			// raise(SIGSEGV);
    	}
    	else
    	{
    		return r;
    	}
	}
}

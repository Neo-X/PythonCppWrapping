
#include "../include/Foo.h"
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>     /* exit, EXIT_FAILURE */
// #include <thread>         // std::this_thread::sleep_for
// #include <chrono>         // std::chrono::seconds


#ifdef _WIN32
    #include <windows.h>

    void _sleep(unsigned milliseconds)
    {
        Sleep(milliseconds);
    }
#else
    #include <unistd.h>

    void _sleep(unsigned milliseconds)
    {
        usleep(milliseconds * 1000); // takes microseconds
    }
#endif

void sighandler(int signum)
{
	printf("Process %d got signal %d\n", getpid(), signum);
	raise(SIGSEGV);
	// _sleep(1000);
    signal(signum, SIG_DFL);
	// std::chrono::milliseconds timespan(111605); // or whatever
	// std::this_thread::sleep_for(timespan);
	// kill(getpid(), signum);
	// exit(-11);
}

extern "C" {
    Foo* Foo_new(){ return new Foo(); }
    void Foo_bar(Foo* foo){ foo->bar(); }
    void Foo_fault(Foo* foo){ foo->fault(); }
    void Foo_raise_fault(Foo * foo) { foo->raise_fault(); }

    int raise_a_fault(int r)
	{
    	signal(SIGSEGV, sighandler);
    	std::cout << "r is "<< r << std::endl;
    	if (r > 3)
    	{
    		// raise(SIGSEGV);
    		volatile int *p = reinterpret_cast<volatile int*>(0);
			*p = 0x1337D00D;
			return 0;
    	}
    	else
    	{
    		return r;
    	}
	}
}

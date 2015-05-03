/*
 * Foo.h
 *
 *  Created on: May 3, 2015
 *      Author: gberseth
 */

#ifndef _FOO_H_
#define _FOO_H_

#include <iostream>
#include <signal.h>

int main()
{
}

class Foo{
    public:
        void bar()
        {
            std::cout << "Hello" << std::endl;
        }
        void fault()
		{
        	char * bad_pointer;
        	bad_pointer[10000] = 'g';
			std::cout << "bad pointer = :" << bad_pointer << std::endl;
		}
        void raise_fault()
        {
        	raise(SIGSEGV);
        }
};
#endif /* _FOO_H_ */


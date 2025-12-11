#include <iostream>
#include <memory>

using namespace std;

struct B; // forward declaration
/*
struct A {
    shared_ptr<B> b_ptr;
    ~A() { cout << "A destroyed\n"; }
};
*/

struct A
{
    weak_ptr<B> b_ptr; // weak_ptr here
    ~A() { cout << "A destroyed\n"; }
};

struct B
{
    shared_ptr<A> a_ptr;
    ~B() { cout << "B destroyed\n"; }
};

int main()
{
    shared_ptr<A> a = make_shared<A>();
    shared_ptr<B> b = make_shared<B>();

    a->b_ptr = b; // weak pointer, no reference increment
    // b->a_ptr = a; // ❌ CIRCULAR REFERENCE: memory never freed
    b->a_ptr = a; // shared ownership

    return 0;
}
#include <bits/stdc++.h>
using namespace std;

int main()
{
    /*
    int *p;  // wild pointer
    *p = 10; // ❌ random memory, crash!
    */

    int *p = nullptr; // safe start
    *p = 10;          // ✅ good for memory allocation

    int *ptr = new int(10);
    delete ptr; // memory freed
    //   cout << *ptr; // ❌ Dangling pointer - undefined behavior

    delete ptr;
    ptr = nullptr; // ✅ now safe

    // 💡 Null Pointer (Modern C++)
    int *p1 = nullptr;

    if (p1 == nullptr)
        cout << "Pointer is null\n";
    else
        cout << "Pointer is valid\n";

    return 0;
}
#include <iostream>
using namespace std;

int main() {
    int x = 10, y = 20;

    // 1. Pointer to constant
    const int *p1 = &x;
    cout << *p1 << endl;  // ✅ Allowed
    // *p1 = 15;          // ❌ Not allowed
    p1 = &y;              // ✅ Allowed

    // 2. Constant pointer
    int *const p2 = &x;
    *p2 = 30;             // ✅ Allowed
    // p2 = &y;            // ❌ Not allowed

    // 3. Constant pointer to constant
    const int *const p3 = &x;
    cout << *p3 << endl;  // ✅ Allowed (read-only)
    // *p3 = 50;          // ❌ Not allowed
    // p3 = &y;           // ❌ Not allowed

    return 0;
}

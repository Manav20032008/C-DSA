#include <iostream>
using namespace std;

int main() {
    int a = 10;
    float b = 3.14;
    char c = 'Z';

    void *ptr; // It can Take any Data Type as Pointing Element 

    ptr = &a;
    cout << "Integer: " << *(int*)ptr << endl;

    ptr = &b;
    cout << "Float: " << *(float*)ptr << endl;

    ptr = &c;
    cout << "Char: " << *(char*)ptr << endl;

    return 0;
}

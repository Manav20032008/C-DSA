#include <iostream>
using namespace std;

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main()
{
    int (*op)(int, int);
    op = add;
    cout << "Sum: " << op(5, 3) << endl;

    op = sub;
    cout << "Difference: " << op(5, 3) << endl;

    return 0;
}

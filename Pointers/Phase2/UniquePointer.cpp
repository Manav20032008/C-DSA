#include <iostream>
#include <memory>
using namespace std;

class Car
{
public:
    Car() { cout << "Car created!\n"; }
    ~Car() { cout << "Car destroyed!\n"; }
    void drive() { cout << "Driving the car...\n"; }
};

int main()
{
    unique_ptr<Car> c1 = make_unique<Car>(); // creation
    c1->drive();

    // unique_ptr cannot be copied
    // unique_ptr<Car> c2 = c1; ❌ ERROR

    // But it can be moved
    unique_ptr<Car> c2 = move(c1); // transfer ownership
    if (!c1)
        cout << "c1 no longer owns the car.\n";
    c2->drive();

    // Automatically destroyed when c2 goes out of scope
}

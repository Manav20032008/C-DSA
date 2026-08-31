#include <iostream>
#include <memory>
using namespace std;

class Student
{
public:
    Student(string n) : name(n) { cout << name << " created!\n"; }
    ~Student() { cout << name << " destroyed!\n"; }
    void show() { cout << "Student: " << name << endl; }

private:
    string name;
};

int main()
{
    shared_ptr<Student> s1 = make_shared<Student>("Manav");
    {
        shared_ptr<Student> s2 = s1; // shared ownership
        cout << "Use count inside block: " << s1.use_count() << endl;
        s2->show();
    } // s2 goes out of scope here

    cout << "Use count after block: " << s1.use_count() << endl;
    s1->show();

    // Auto deleted after s1 also goes out of scope
}

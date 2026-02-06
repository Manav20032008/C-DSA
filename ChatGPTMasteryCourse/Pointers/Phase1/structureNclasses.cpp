#include <iostream>
using namespace std;

struct Student
{
    string name;
    int age;
};

int main()
{
    Student *s = new Student;
    s->name = "Manav";
    s->age = 21;

    cout << s->name << " is " << s->age << " years old." << endl;

    delete s;
    return 0;
}

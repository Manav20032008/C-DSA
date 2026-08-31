#include <iostream>
#include <string>
using namespace std;

struct Book
{
    string title;
    string author;
    double price;
};

// Function that returns a dynamically allocated Book*
Book *createBook(string title, string author, double price)
{
    Book *b = new Book;
    b->title = title;
    b->author = author;
    b->price = price;
    return b;
}

int main()
{
    int n;
    cout << "Enter the size of the array that you want to create: ";
    cin >> n;

    // Dynamic ARRAY of POINTERS
    Book **arr = new Book *[n];

    // Input
    for (int i = 0; i < n; i++)
    {
        string Title, Author;
        double Price;

        cout << "Enter Title, Author, Price for book " << i + 1 << ": ";
        cin >> Title >> Author >> Price;

        arr[i] = createBook(Title, Author, Price); // store pointer
    }

    // Output
    cout << "\n===== BOOK DETAILS =====\n";
    for (int i = 0; i < n; i++)
    {
        cout << "\nBook " << i + 1 << ":\n";
        cout << "Title: " << arr[i]->title << endl;
        cout << "Author: " << arr[i]->author << endl;
        cout << "Price: " << arr[i]->price << endl;
    }

    // FREE MEMORY (very important!)
    for (int i = 0; i < n; i++)
    {
        delete arr[i]; // delete each Book object
    }

    delete[] arr;
    
    return 0;
}

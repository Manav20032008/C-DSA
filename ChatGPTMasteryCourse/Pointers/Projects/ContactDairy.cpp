#include <bits/stdc++.h>
using namespace std;

struct contact
{
    string Name, mobileNo, emailId;
    contact *next;
};

// To Add The Contact In The Dairy 
void addContact(contact *&head, string name, string mobileno, string email)
{
    contact *newContact = new contact();
    newContact->Name = name;
    newContact->mobileNo = mobileno;
    newContact->emailId = email;
    newContact->next = nullptr;

    if (head == nullptr)
    {
        head = newContact;
        return;
    }

    contact *temp = head;
    while (temp->next != nullptr)
    {
        temp = temp->next;
    }
    temp->next = newContact;
}

// To Watch The All The Contacts In the Dairy
void displayContact(contact *head)
{
    if (head == nullptr)
    {
        cout << "No contacts to display!\n";
        return;
    }

    contact *temp = head;
    while (temp != nullptr)
    {
        cout << "[" << temp->Name << " - " << temp->mobileNo << " | " << temp->emailId << "]" << endl;
        temp = temp->next;
    }
    cout << "Diary Completed!\n";
}

// To Find The Contact In The Dairy 

void searchContact(contact *head, string name)
{
    contact *curr = head;
    while (curr != nullptr && curr->Name != name)
    {
        curr = curr->next;
    }
    cout << "[" << curr->Name << " - " << curr->mobileNo << " | " << curr->emailId << "]" << endl;
}

// To Detele The Contact From The Dairy 

void deleteContact(contact *&head, string name)
{
    if (head == nullptr)
        return;

    if (head->Name == name)
    {
        contact *temp = head;
        head = head->next;
        delete temp;
        return;
    }

    contact *curr = head;
    contact *prev = nullptr;

    while (curr != nullptr && curr->Name != name)
    {
        prev = curr;
        curr = curr->next;
    }

    if (curr == nullptr)
    {
        cout << "Contact not found!" << endl;
        return;
    }
    prev->next = curr->next;
    delete curr;
}

int main()
{
    bool flag = true;
    contact *head = nullptr;
    do
    {
        int choice;
        cout << "\n----- CONTACT BOOK MENU -----\n";
        cout << "1.Add Contact \n2.Dispaly Contacts \n3.Search Contact \n4.Delete Contact \n5.Exit \n";
        cout << "-----------------------------\n";
        cout << "Enter your choice: ";
        cin >> choice;
        switch (choice)
        {
        case 1:
        {
            string name, mobileno, emailid;
            cout << "Enter The Name, Mobile No And Email Id: ";
            cin >> name >> mobileno >> emailid;
            addContact(head, name, mobileno, emailid);
            break;
        }
        case 2:
        {
            displayContact(head);
            break;
        }
        case 3:
        {
            string name;
            cout << "Enter the Name Of Person To Search: ";
            cin >> name;
            searchContact(head, name);
            break;
        }
        case 4:
        {
            string name;
            cout << "Enter the Name Of Person To Delete: ";
            cin >> name;
            deleteContact(head, name);
            break;
        }
        case 5:
        {
            flag = false;
            break;
        }
        default:
        {
            cout << "Invalid choice! Please try again.\n";
        }
        }

    } while (flag);

    cout << " Thank you For Using Program !";
    return 0;
}
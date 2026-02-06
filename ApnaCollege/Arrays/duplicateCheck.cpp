// Amazon Interview Qs

#include <iostream>
using namespace std;

int duplicateCheck(int arr[], int num)
{
    for (int i = 0; i < num - 1; i++)   // loop till second last
    {
        for (int j = i + 1; j < num; j++)   // check all next elements
        {
            if (arr[i] == arr[j])   // if duplicate found
            {
                return 1;
            }
        }
    }
    return 0;   // no duplicates found
}

int main()
{
    int arr[] = {4, 1, 2, 1, 2};
    int num = 5;

    int result = duplicateCheck(arr, num);

    if (result == 1)
    {
        cout << "This Array Contains Duplicate Elements";
    }
    else
    {
        cout << "This Array Doesn't Contain Duplicate Elements";
    }

    return 0;
}

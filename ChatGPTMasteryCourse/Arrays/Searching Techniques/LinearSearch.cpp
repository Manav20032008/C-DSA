#include <bits/stdc++.h>
using namespace std;

int main()
{
    // BEST {UNSORTED ARRAY}
    int arr[] = {4, 6, 9, 3, 7, 5};
    int target = 6;

    // Linear Searching Technique
    for (int i = 0; i < 6; i++)
    {
        if (arr[i] == target)
        {
            cout << arr[i];
            break;
        }
    }
    
    /*
    Time Complexity:- O(n)
    Space Complexity:- O(n)
    */

    return 0;
}
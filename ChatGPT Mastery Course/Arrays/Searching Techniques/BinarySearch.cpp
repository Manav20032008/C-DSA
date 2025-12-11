#include <bits/stdc++.h>
using namespace std;

int main()
{
    // BEST {SORTED ARRAY}
    int arr[] = {3, 4, 5, 6, 7, 9};
    int target = 6;

    // Binary Search
    int start = 0, end = 5;
    while (start < end)
    {
        int mid = end + (start - end) / 2;
        if (arr[mid] == target)
        {
            cout << arr[mid];
        }
        else if (arr[mid] > target)
        {
            end = mid - 1;
        }
        else
        {
            start = mid + 1;
        }
    }

    /*
    Time Complexity:- O(log(n))
    Space Complexity:- O(n)
    */

    return 0;
}
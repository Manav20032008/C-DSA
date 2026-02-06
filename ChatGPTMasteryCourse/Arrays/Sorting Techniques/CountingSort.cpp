#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[] = {4, 2, 2, 8, 3, 3, 1};

    // Counting Sorting Technique
    int maxVal = arr[0];
    for (int i = 1; i < 7; i++)
        maxVal = max(maxVal, arr[i]);

    vector<int> count(maxVal + 1, 0);
    vector<int> output(7);

    // Count occurrences
    for (int i = 0; i < 7; i++)
        count[arr[i]]++;

    // * Prefix sum
    for (int i = 1; i <= maxVal; i++)
        count[i] += count[i - 1];

    // Build output array (stable)
    for (int i = 6; i >= 0; i--)
    {
        output[count[arr[i]] - 1] = arr[i];
        count[arr[i]]--;
    }

    // Copy back
    for (int i = 0; i < 7; i++)
        arr[i] = output[i];

        
    /*
    Time Complexity:- O(n)
    Space Complexity:- O(n)
    */

    for (int i = 0; i < 7; i++)
    {
        cout << arr[i] << " ";
    }

    return 0;
}
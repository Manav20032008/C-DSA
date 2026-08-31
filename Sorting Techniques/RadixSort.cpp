#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[] = {4, 2, 2, 8, 3, 3, 1};

    // Radix Sorting Technique

    int maxVal = arr[0];
    for (int i = 1; i < 7; i++)
        maxVal = max(maxVal, arr[i]);

    for (int exp = 1; maxVal / exp > 0; exp *= 10)
    { // Repeating Counting Sort

        vector<int> count(10, 0);
        vector<int> output(7);

        // Count occurrences
        for (int i = 0; i < 7; i++)
        {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }

        // * Prefix sum
        for (int i = 1; i < 10; i++)
            count[i] += count[i - 1];

        // Build output array (stable)
        for (int i = 6; i >= 0; i--)
        {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }

        // Copy back
        for (int i = 0; i < 7; i++)
            arr[i] = output[i];
    }

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
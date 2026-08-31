#include <bits/stdc++.h>
using namespace std;

int main()
{
    // only For Element In Range 0 to 1
    float arr[] = {0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51};

    // Bucket Sorting Technique
    vector<float> bucket[7];

    // Insert elements into buckets
    for (int i = 0; i < 7; i++)
    {
        int idx = 7 * arr[i];
        bucket[idx].push_back(arr[i]);
    }

    // Sort each bucket
    for (int i = 0; i < 7; i++)
        sort(bucket[i].begin(), bucket[i].end());

    // Concatenate
    int k = 0;
    for (int i = 0; i < 7; i++)
        for (float x : bucket[i])
            arr[k++] = x;

    /*
    Time Complexity:- O(nlog(n))
    Space Complexity:- O(n)
    */

    for (int i = 0; i < 7; i++)
    {
        cout << arr[i] << " ";
    }
    return 0;
}
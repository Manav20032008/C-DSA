#include <bits/stdc++.h>
using namespace std;

void merge(int arr[], int low, int mid, int high)
{
    vector<int> temp;         // Duplicate array
    int i = low, j = mid + 1; // Two Pointers Approach To Sorted Merge

    while (i <= mid && j <= high)
    { // When Both Are Non-Empty
        if (arr[i] <= arr[j])
        {
            temp.push_back(arr[i]);
            i++;
        }
        else
        {
            temp.push_back(arr[j]);
            j++;
        }
    }

    while (i <= mid)
    { // One Of Them Is Empty
        temp.push_back(arr[i]);
        i++;
    }

    while (j <= high)
    { // One Of Them Is Empty
        temp.push_back(arr[j]);
        j++;
    }

    // copying the Temporary Array Into Original One
    for (int i = 0; i < temp.size(); i++)
    {
        arr[low + i] = temp[i];
    }
}

void mergeSort(int arr[], int low, int high)
{
    if (low >= high)
        return;

    int mid = low + (high - low) / 2;
    mergeSort(arr, low, mid);      // left divided part sorting
    mergeSort(arr, mid + 1, high); // right divided part sorting

    merge(arr, low, mid, high); // Reverse Merging 2 Sorted Array in Big Array
}

int main()
{
    int arr[] = {4, 6, 9, 3, 7, 5};

    // Merge Sorting Techniques
    mergeSort(arr, 0, 4);

    /*
    Time Complexity:- O(nlog(n))
    Space Complexity:- O(n)
    */

    for (int i = 0; i < 5; i++)
    {
        cout << arr[i] << " ";
    }
    return 0;
}
#include <bits/stdc++.h>
using namespace std;

int partition(int arr[], int low, int high)
{
    int pivot = arr[high]; // Assuming Highest Part As highest

    int i = low - 1; // Two-Pointers Approach to Find the Original Position OF The Pivot
    for (int j = low; j < high; j++)
    {
        if (arr[j] < pivot)
        {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);

    return i + 1; // Returning Pivot For Next Divided Iteration
}

void quickSort(int arr[], int low, int high)
{
    if (low < high)  // condition till Sorting Continue
    {
        int pivot = partition(arr, low, high); // Deciding the Pivot with It's Original Position

        quickSort(arr, low, pivot - 1);        // Left Divided Part Of Sorting
        quickSort(arr, pivot + 1, high);       // Right Divided Part Of Sorting
    }
}

int main()
{
    int arr[] = {4, 6, 9, 3, 7, 5};

    // Quick Sorting Techniques
    quickSort(arr, 0, 4);

    /*
    Time Complexity:- O(n^2)
    Space Complexity:- O(n)
    */

    for (int i = 0; i < 5; i++)
    {
        cout << arr[i] << " ";
    }
    return 0;
}
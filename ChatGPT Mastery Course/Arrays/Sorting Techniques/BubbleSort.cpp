#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[] = {4, 6, 9, 3, 7, 5};

    // Bubble Sorting Technique
    for (int i = 0; i < 5; i++)
    {
        // Bubbling the Highest Element Of Array at Last One By One 
        for (int j = 0; j < 5 - i /* reducing size of array */; j++)
        {
            if (arr[j] > arr[i + 1])
            {
                swap(arr[j], arr[i + 1]);
            }
        }
    }

    /*
    Time Complexity:- O(n^2)
    Space Complexity:- O(n)
    */

    for(int i = 0 ; i < 5 ; i++){
        cout << arr[i] << " ";
    }

    return 0;
}
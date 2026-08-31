#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[] = {4, 6, 9, 3, 7, 5};

    // Selection Sorting Technique
    int minIndex = -1 ;
    for (int i = 0; i < 5; i++)
    {
        // Selecting the Minimum number and putting it at first 
        for (int j = i + 1 ; j < 5 ; j++)
        {
            if (arr[j] < arr[minIndex])
            {
                minIndex = j ; // Finding the Minimum Element Of the Array
            }

            swap(arr[i],arr[minIndex]); 
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
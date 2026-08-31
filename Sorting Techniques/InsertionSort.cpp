#include <bits/stdc++.h>
using namespace std;

int main()
{
    int arr[] = {4, 6, 9, 3, 7, 5};

    // Insertion Sorting Technique
    for(int i = 0 ; i < 6 ; i++){
        int key = arr[i] ;
        int j ; 
        for(j = 5 ; j >= 0 && arr[j] > key ; j--){
            arr[j+1] = arr[j];
        }
        arr[j+1] = key ;
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
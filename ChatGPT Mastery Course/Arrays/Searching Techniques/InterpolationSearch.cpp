#include <bits/stdc++.h>
using namespace std;

int main()
{
    // only for {SORTED ARRAY}
    int arr[] = {3, 4, 5, 6, 7, 9};
    int target = 6;

    
    // Interpolation Searching Technique
    int low = 0 , high = 5 ;
    while(low <= high && target >= arr[low] && target <= arr[high]){
        if(low == high){
            (arr[low] == target) ? cout << arr[low] : cout << "Element Not Found !" ;
        }

        // * Estimating The Position Using Interpolation formula
        int pos = low + ((double)(high - low) / (arr[high] - arr[low])) * (target - arr[low]);

        if(arr[pos] == target) cout << arr[pos] ;
        if(arr[pos] < target) low = pos + 1 ;
        else high = pos - 1 ;
    }
    
    /*
    Time Complexity:- O(n)
    Space Complexity:- O(n)
    */

    return 0;
}
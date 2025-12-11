#include <bits/stdc++.h>
using namespace std;

int main()
{
    // only for {SORTED ARRAY}
    int arr[] = {3, 4, 5, 6, 7, 9};
    int target = 6;

    
    // Exponential Searching Technique
    if(arr[0] == target) cout << arr[0] ;

    int i = 1 ;
    while( i < 6 && arr[i] <= target){
        i *= 2 ;
    }

    // then binary search for low = i / 2 , high = min(i , 5) ;
    
    /*
    Time Complexity:- O(log(n))
    Space Complexity:- O(n)
    */

    return 0;
}
#include <bits/stdc++.h>
using namespace std;

int main()
{
    // only for {SORTED ARRAY}
    int arr[] = {3, 4, 5, 6, 7, 9};
    int target = 6;

    
    // Jump Searching Technique
    int step = sqrt(6) ;
    int prev = 0 ;

    while(arr[step-1] < target){ // loopto find the block by which we can perform small search
        prev = step ;
        step += sqrt(6);
        if(prev >= 6) cout << "Element Not Found!" ;
    }

    for(int i = prev ; i < step ; i++){ // linear search for small block
        if(arr[i] == target) cout << arr[i] ;
    }
    
    /*
    Time Complexity:- O(sqrt(n))
    Space Complexity:- O(n)
    */

    return 0;
}
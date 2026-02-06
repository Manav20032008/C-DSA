// Microsoft + Facebook Interview Qs

#include <iostream>
#include <limits.h>
using namespace std;

int main(){
    int arr[] = { 3, 7, -9, 6, -1, 4, -7, 2};
    int num = sizeof(arr) / sizeof(arr[0]);

    int maxSum = INT_MIN ;
    int currentSum = 0 ;

    for(int i = 0; i < num; i++){
        currentSum += arr[i] ;
        maxSum = max(currentSum,maxSum) ;
        
        if(currentSum < 0){
            currentSum = 0 ;
        }
    }

    cout << "Maximum Subarray Sum = " << maxSum << endl;

return 0 ;
}


/* BRUTE FORCE:-

Find All Possible Sub-Array And Then Find That The Which Sub-Array Has Maximum Number Of Sum.

*/
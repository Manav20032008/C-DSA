#include <bits/stdc++.h>
using namespace std;

int main(){
    int n ; 
    cout << "Enter The Size Of the Array:" ;
    cin >> n;

    // Dynamic Allocation Of Array
    int *arr = new int[n] ;
    for(int i = 0 ; i < n ; i++){
        cout << "Enter The " << i + 1 << "th Element Of The Array:" ;
        cin >> arr[i];
    }

    for(int i = 0 ; i < n ; i++){
        cout << "The " << i + 1 << "th Element Of The Array is " << arr[i] << endl ;
    }

    // Resize The Array
    int newSize ;
    cout << "Enter The New Size Of The Array:" ;
    cin >> newSize ;

    int *arr1 = new int[newSize];

    // Copy The Old Array into New Big Array
    for(int i = 0 ; i < n ; i++){
        arr1[i] = arr[i] ;
    }

    //Fill The Reamining Data With '0'
    for(int j = n ; j < newSize ; j++){
        arr1[j] = 0 ;
    }

    for(int i = 0 ; i < newSize ; i++){
        cout << "The " << i + 1 << "th Element Of The Array is " << arr1[i] << endl ;
    }

    delete[] arr ;


return 0 ;
}
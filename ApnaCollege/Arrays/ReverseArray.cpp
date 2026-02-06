// Infosys Moonfrog Labs

#include <iostream>
using namespace std;

void reversedArray(int arr[], int num){
    int rev_array[num] ;
    int i = 0;

    for(int k = num-1; k >= 0; k--){
        rev_array[i] = arr[k] ;
        i++ ;
    }

    for(int j = 0; j <= num-1; j++){
        cout << rev_array[j] << "  ";
    }
}

int main()
{
    int arr[] = {1, 2, 3, 4, 5};
    int num = 5 ;
    
    reversedArray(arr, num);


    return 0;
}
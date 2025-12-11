// Amazon Interview Qs

#include <iostream>
#include <algorithm> // for sort
using namespace std;

int main(){
    int arr[] = {97, 43, 82, 74, 69, 12, 56};
    int num = sizeof(arr) / sizeof(arr[0]);
    int student = 4;

    // Sort in ascending order
    sort(arr, arr + num);

    int chocolateArray[student - 1];
    for(int i = 0; i < student ; i++){
        chocolateArray[i] = arr[i];  
        cout << "The Packet Size:" << chocolateArray[i] << "\n";
    }

    cout << "The Difference Between Max And Min is:" << chocolateArray[student - 1] -  chocolateArray[0];

return 0 ;
}
// ABCO Accolite Amazon Cisco Hike Microsoft Snapdeal VMWare Google Adobe

#include <iostream>
#include <climits> // usefull for using INT__MIN / INT__MAX
using namespace std;

int maxElement(int arr[], int num)
{
    int max = INT_MIN;
    for (int i = 0; i <= num; i++) // loop for traversing each elements of array
    {
        if (arr[i] >= max) // logical condition for storing max value
        {
            max = arr[i];
        }
    }
    return max;
}

int minElement(int arr[], int num)
{
    int min = INT_MAX;
    for (int i = 0; i <= num; i++) // loop for traversing each elements of array
    {
        if (arr[i] <= min) // logical condition for storing min value
        {
            min = arr[i];
        }
    }
    return min;
}

int main()
{
    int arr[] = {3, 7, 1, 9, 5 , 13};
    int num = 5;

    int max = maxElement(arr, num); 
    int min = minElement(arr, num);

    cout << "The Maximum Element In Array is " << max << "\n";
    cout << "The Minimum Element In Array is " << min << "\n";
    return 0;
}





/* SORTING METHOD 

-> Sort the Array 
-> First Element will be Min & Last element will be Max
*/

/* TOURNAMENT PAIRING METHOD


// C++ program of above implementation 
#include<bits/stdc++.h> 
using namespace std; 

// Structure is used to return 
// two values from minMax() 
struct Pair 
{ 
    int min; 
    int max; 
}; 

struct Pair getMinMax(int arr[], int n) 
{ 
    struct Pair minmax;     
    int i; 
    
    // If array has even number of elements 
    // then initialize the first two elements 
    // as minimum and maximum 
    if (n % 2 == 0) 
    { 
        if (arr[0] > arr[1])     
        { 
            minmax.max = arr[0]; 
            minmax.min = arr[1]; 
        } 
        else
        { 
            minmax.min = arr[0]; 
            minmax.max = arr[1]; 
        } 
        
        // Set the starting index for loop 
        i = 2; 
    } 
    
    // If array has odd number of elements 
    // then initialize the first element as 
    // minimum and maximum 
    else
    { 
        minmax.min = arr[0]; 
        minmax.max = arr[0]; 
        
        // Set the starting index for loop 
        i = 1; 
    } 
    
    // In the while loop, pick elements in 
    // pair and compare the pair with max 
    // and min so far 
    while (i < n - 1) 
    {         
        if (arr[i] > arr[i + 1])         
        { 
            if(arr[i] > minmax.max)     
                minmax.max = arr[i]; 
                
            if(arr[i + 1] < minmax.min)         
                minmax.min = arr[i + 1];     
        } 
        else        
        { 
            if (arr[i + 1] > minmax.max)     
                minmax.max = arr[i + 1]; 
                
            if (arr[i] < minmax.min)         
                minmax.min = arr[i];     
        } 
        
        // Increment the index by 2 as 
        // two elements are processed in loop 
        i += 2; 
    }         
    return minmax; 
} 

// Driver code 
int main() 
{ 
    int arr[] = { 1000, 11, 445, 
                1, 330, 3000 }; 
    int arr_size = 6; 
    
    Pair minmax = getMinMax(arr, arr_size); 
    
    cout << "Minimum element is "
        << minmax.min << endl; 
    cout << "Maximum element is "
        << minmax.max; 
        
    return 0; 
} 

// This code is contributed by nik_3112
*/
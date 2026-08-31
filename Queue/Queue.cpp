#include <bits/stdc++.h>
using namespace std;

class Queue{
    public:
    int array[10];
    int front ,rear = -1 ;

    void enqueue(int num){
        if((front + 1) % 10 == rear){
            cout << "Queue IS Full.\n";
        }else{
            if(front == -1){
                front++;
                rear++;
                array[rear] = num ;
            }else{
                rear = (rear + 1) % 10 ;
                array[rear] = num;
            }
        }
    }

    void dequeue(){
        if(front == -1){
            cout << "Queue Is Empty.\n";
        }else{
            if(front == rear){
                front = -1; 
                rear = -1;
            }else{
                front = (front + 1) % 10 ;
            }
        }
    }

    void display(){
        for(int i = front ; ; i = (i + 1) % 10){
            if(i >= rear){
                break ;
            }else{
                cout << array[i];
            }
        }
    }
};

int main(){
    
return 0;
}
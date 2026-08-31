#include <bits/stdc++.h>
using namespace std;

class Stack{
    public:
    int array[10];
    int top = -1;

    void push(int num){
        if(top == 9){
            cout << "Stack Is Full.\n";
        }else{
            top++;
            array[top] = num;
        }
    }

    void pop(){
        if(top == -1){
            cout << "Stack IS Empty.\n";
        }else{
            top--;
        }
    }

    int peek(){
        if(top != -1){
            return array[top];
        }
        else{
            return -1; 
        }
    }

    void display(){
        for(int i = 0 ; i < 10 ; i++){
            cout << array[i] << endl;
        }
    }

};

int main(){
    Stack s ;

    s.push(10);
    s.push(20);
    s.push(30);
    s.display();

    s.pop();
    s.peek();
    
return 0;
}
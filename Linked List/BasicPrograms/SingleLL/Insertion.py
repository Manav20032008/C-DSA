class Node:
    def __init__ (self, data , next = None):
        self.data = data
        self.next = next

class Solution :
    def insertAtHead(self,head,newData):
        newNode = Node(newData,head)
        return newNode

    def insertAtTail(self,head,newData):
        temp = head 

        while temp.next :
            temp = temp.next

        node = Node(newData)
        temp.next = node

    

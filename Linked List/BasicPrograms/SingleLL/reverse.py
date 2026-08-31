class Node:
    def __init__ (self, data , next = None):
        self.data = data
        self.next = next

class Solution(object):
    def reverseList(self, head):
        curr = head
        prev = None

        while curr :
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        
        return prev
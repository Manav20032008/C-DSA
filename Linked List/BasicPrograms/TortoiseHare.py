class Node:
    def __init__ (self, data , next = None):
        self.data = data
        self.next = next


class Solution(object):

    def middleNode(self, head):

        if not head or not head.next :
            return head
        slow , fast = head , head 

        while fast and fast.next :
            slow = slow.next
            fast = fast.next.next
            
        return slow 
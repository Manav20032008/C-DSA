class Node:
    def __init__ (self, data , next = None):
        self.data = data
        self.next = next

class Solution :

    def deleteTail(self, head):
        if head is None or head.next is None:
            return None

        curr = head
        while curr.next.next is not None:
            curr = curr.next

        curr.next = None
        return head
class Node:
    def __init__(self, val):
        self.data = val
        self.next = None

class Solution:
    def searchValue(self, head, key):
        current = head

        while current is not None:
            if current.data == key:
                return True
            current = current.next

        return False

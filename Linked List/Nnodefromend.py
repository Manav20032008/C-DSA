'''
19. Remove Nth Node From End of List
Given the head of a linked list, remove the nth node from the end of the list and return its head.

 

Example 1:


Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
'''


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def removeNthFromEnd(self, head, n):
        if not head or not head.next:
            return None

        fast = head
        slow = head

        for i in range(n):
            fast = fast.next
        
        if not fast:
            return head.next
            
        while fast.next :
            fast = fast.next 
            slow = slow.next
        
        slow.next = slow.next.next
        return head
        
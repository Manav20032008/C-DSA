class Node:
    def __init__(self, val):
        self.data = val
        self.next = None
        self.prev = None

def convert_list_to_dll(arr):
    head = Node(arr[0])
    prev = head

    for i in range(1, len(arr)):
        new_node = Node(arr[i])
        new_node.prev = prev
        prev.next = new_node
        prev = new_node

    return head
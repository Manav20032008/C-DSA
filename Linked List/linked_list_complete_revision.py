"""
LINKED LIST — COMPLETE REVISION FILE
====================================

Purpose:
    A single Python revision file for placement/interview preparation.

Covers:
    1. Singly Linked List
    2. Doubly Linked List
    3. Circular Linked List
    4. CRUD operations
    5. Pointer manipulation
    6. Fast/slow pointer techniques
    7. Reversal patterns
    8. Cycle detection/removal
    9. Merge operations
    10. Palindrome
    11. Intersection
    12. Nth node from end
    13. Reordering / rotation
    14. Sorting
    15. Duplicate removal
    16. Advanced interview patterns
    17. Complexity cheat sheet

Use this file as a 2-month pre-placement revision library.
Try to implement each algorithm yourself before reading the function.

Python only.
"""

# ============================================================
# 0. COMPLEXITY CHEAT SHEET
# ============================================================

"""
SINGLY LINKED LIST
------------------
Access by index       O(n)
Search                O(n)
Insert at head        O(1)
Insert at tail        O(1) with tail pointer, otherwise O(n)
Delete head           O(1)
Delete tail           O(n) generally
Reverse               O(n)
Find middle           O(n)
Detect cycle          O(n) time, O(1) space

DOUBLY LINKED LIST
------------------
Access by index       O(n)
Search                O(n)
Insert at head        O(1)
Insert at tail        O(1) with tail pointer
Delete known node     O(1)
Reverse               O(n)

CIRCULAR LINKED LIST
--------------------
Traversal             O(n)
Insert after known node O(1)
Delete after known node O(1)
Search                O(n)

COMMON PATTERNS
---------------
Fast/slow pointers    O(n), O(1)
Merge sorted lists    O(n + m)
Palindrome            O(n), O(1)
Cycle detection       O(n), O(1)
Cycle entry           O(n), O(1)
Merge sort             O(n log n)
"""


# ============================================================
# 1. SINGLY LINKED LIST
# ============================================================

class SinglyNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f"SinglyNode({self.value!r})"


class SinglyLinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0

        if values:
            for value in values:
                self.append(value)

    # -------------------------
    # Traversal
    # -------------------------

    def to_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.value)
            current = current.next

        return result

    def display(self):
        print(" -> ".join(map(str, self.to_list())) + " -> None")

    # -------------------------
    # CRUD: Create / Read
    # -------------------------

    def prepend(self, value):
        node = SinglyNode(value)
        node.next = self.head
        self.head = node

        if self.tail is None:
            self.tail = node

        self.size += 1
        return node

    def append(self, value):
        node = SinglyNode(value)

        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.size += 1
        return node

    def insert_at(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        if index == 0:
            return self.prepend(value)

        if index == self.size:
            return self.append(value)

        prev = self.head
        for _ in range(index - 1):
            prev = prev.next

        node = SinglyNode(value)
        node.next = prev.next
        prev.next = node

        self.size += 1
        return node

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        return current.value

    def find(self, value):
        current = self.head
        index = 0

        while current:
            if current.value == value:
                return index

            current = current.next
            index += 1

        return -1

    # -------------------------
    # Delete
    # -------------------------

    def delete_head(self):
        if self.head is None:
            return None

        removed = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        self.size -= 1
        removed.next = None

        return removed.value

    def delete_value(self, value):
        if self.head is None:
            return False

        if self.head.value == value:
            self.delete_head()
            return True

        prev = self.head
        current = self.head.next

        while current:
            if current.value == value:
                prev.next = current.next

                if current is self.tail:
                    self.tail = prev

                current.next = None
                self.size -= 1
                return True

            prev = current
            current = current.next

        return False

    def delete_at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        if index == 0:
            return self.delete_head()

        prev = self.head

        for _ in range(index - 1):
            prev = prev.next

        removed = prev.next
        prev.next = removed.next

        if removed is self.tail:
            self.tail = prev

        removed.next = None
        self.size -= 1

        return removed.value

    # -------------------------
    # Update
    # -------------------------

    def update(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        current.value = value

    # ========================================================
    # Core Linked List Algorithms
    # ========================================================

    def reverse_iterative(self):
        """
        Classic three-pointer reversal.

        prev <- current <- next
        """
        prev = None
        current = self.head

        self.tail = self.head

        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        self.head = prev
        return self.head

    def reverse_recursive(self):
        def reverse(node):
            if node is None or node.next is None:
                return node

            new_head = reverse(node.next)

            node.next.next = node
            node.next = None

            return new_head

        self.tail = self.head
        self.head = reverse(self.head)

        return self.head

    def middle_node(self):
        """
        Slow moves 1 step, fast moves 2 steps.
        For even length, returns the second middle.
        """
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow

    def nth_from_end(self, n):
        """
        Returns the nth node from the end.
        n=1 means last node.
        """
        if n <= 0:
            raise ValueError("n must be positive")

        fast = slow = self.head

        for _ in range(n):
            if fast is None:
                raise IndexError("n is larger than list length")
            fast = fast.next

        while fast:
            slow = slow.next
            fast = fast.next

        return slow

    def remove_nth_from_end(self, n):
        dummy = SinglyNode(0)
        dummy.next = self.head

        fast = slow = dummy

        for _ in range(n + 1):
            if fast is None:
                raise IndexError("n is larger than list length")
            fast = fast.next

        while fast:
            slow = slow.next
            fast = fast.next

        removed = slow.next
        slow.next = removed.next

        if removed is self.tail:
            self.tail = slow if slow is not dummy else None

        self.head = dummy.next
        self.size -= 1

        return removed.value

    # -------------------------
    # Cycle Detection
    # -------------------------

    def has_cycle(self):
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                return True

        return False

    def cycle_entry(self):
        """
        Floyd's algorithm:
        Phase 1 -> detect meeting point.
        Phase 2 -> move one pointer to head.
        Both move one step; their meeting point is cycle entry.
        """
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                break
        else:
            return None

        slow = self.head

        while slow is not fast:
            slow = slow.next
            fast = fast.next

        return slow

    def cycle_length(self):
        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                length = 1
                current = slow.next

                while current is not slow:
                    length += 1
                    current = current.next

                return length

        return 0

    def remove_cycle(self):
        entry = self.cycle_entry()

        if entry is None:
            return False

        current = entry

        while current.next is not entry:
            current = current.next

        current.next = None
        self.tail = current

        return True

    # -------------------------
    # Palindrome
    # -------------------------

    def is_palindrome(self):
        if self.head is None or self.head.next is None:
            return True

        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        second_half = reverse_nodes(slow)

        first = self.head
        second = second_half

        palindrome = True

        while second:
            if first.value != second.value:
                palindrome = False
                break

            first = first.next
            second = second.next

        reverse_nodes(second_half)

        return palindrome

    # -------------------------
    # Duplicate Removal
    # -------------------------

    def remove_duplicates_sorted(self):
        current = self.head

        while current and current.next:
            if current.value == current.next.value:
                current.next = current.next.next
                self.size -= 1
            else:
                current = current.next

        self.tail = current
        return self

    def remove_duplicates_unsorted(self):
        seen = set()
        current = self.head
        prev = None

        while current:
            if current.value in seen:
                prev.next = current.next
                if current is self.tail:
                    self.tail = prev
                self.size -= 1
            else:
                seen.add(current.value)
                prev = current

            current = current.next

        return self

    # -------------------------
    # Rotate
    # -------------------------

    def rotate_right(self, k):
        if self.head is None or self.head.next is None or k == 0:
            return self

        k %= self.size

        if k == 0:
            return self

        # Make circular temporarily.
        self.tail.next = self.head

        steps_to_new_tail = self.size - k
        new_tail = self.head

        for _ in range(steps_to_new_tail - 1):
            new_tail = new_tail.next

        self.head = new_tail.next
        new_tail.next = None
        self.tail = new_tail

        return self

    # -------------------------
    # Sorting
    # -------------------------

    def sort(self):
        self.head = merge_sort_nodes(self.head)
        self.tail = self.head

        if self.tail:
            while self.tail.next:
                self.tail = self.tail.next

        return self

    # -------------------------
    # Reorder
    # -------------------------

    def reorder(self):
        """
        L0 -> Ln -> L1 -> Ln-1 -> ...
        """
        if self.head is None or self.head.next is None:
            return self

        slow = fast = self.head

        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None
        second = reverse_nodes(second)

        first = self.head

        while second:
            first_next = first.next
            second_next = second.next

            first.next = second
            second.next = first_next

            first = first_next
            second = second_next

        self.tail = self.head

        while self.tail.next:
            self.tail = self.tail.next

        return self


# ============================================================
# 2. DOUBLY LINKED LIST
# ============================================================

class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"DoublyNode({self.value!r})"


class DoublyLinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0

        if values:
            for value in values:
                self.append(value)

    def to_list(self):
        result = []
        current = self.head

        while current:
            result.append(current.value)
            current = current.next

        return result

    def to_reverse_list(self):
        result = []
        current = self.tail

        while current:
            result.append(current.value)
            current = current.prev

        return result

    def display(self):
        print(" <-> ".join(map(str, self.to_list())) + " <-> None")

    def prepend(self, value):
        node = DoublyNode(value)

        node.next = self.head

        if self.head:
            self.head.prev = node
        else:
            self.tail = node

        self.head = node
        self.size += 1

        return node

    def append(self, value):
        node = DoublyNode(value)

        node.prev = self.tail

        if self.tail:
            self.tail.next = node
        else:
            self.head = node

        self.tail = node
        self.size += 1

        return node

    def insert_after(self, node, value):
        if node is None:
            raise ValueError("node cannot be None")

        new_node = DoublyNode(value)

        new_node.prev = node
        new_node.next = node.next

        if node.next:
            node.next.prev = new_node
        else:
            self.tail = new_node

        node.next = new_node
        self.size += 1

        return new_node

    def insert_before(self, node, value):
        if node is None:
            raise ValueError("node cannot be None")

        new_node = DoublyNode(value)

        new_node.next = node
        new_node.prev = node.prev

        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node

        node.prev = new_node
        self.size += 1

        return new_node

    def delete_node(self, node):
        if node is None:
            return None

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None
        self.size -= 1

        return node.value

    def find(self, value):
        current = self.head

        while current:
            if current.value == value:
                return current

            current = current.next

        return None

    def reverse(self):
        current = self.head

        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev

        self.head, self.tail = self.tail, self.head

        return self

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0


# ============================================================
# 3. CIRCULAR SINGLY LINKED LIST
# ============================================================

class CircularNode:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f"CircularNode({self.value!r})"


class CircularLinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0

        if values:
            for value in values:
                self.append(value)

    def to_list(self):
        result = []

        if self.head is None:
            return result

        current = self.head

        while True:
            result.append(current.value)
            current = current.next

            if current is self.head:
                break

        return result

    def display(self):
        if self.head is None:
            print("Empty")
            return

        print(" -> ".join(map(str, self.to_list())) + " -> HEAD")

    def append(self, value):
        node = CircularNode(value)

        if self.head is None:
            self.head = self.tail = node
            node.next = node
        else:
            node.next = self.head
            self.tail.next = node
            self.tail = node

        self.size += 1
        return node

    def prepend(self, value):
        node = CircularNode(value)

        if self.head is None:
            self.head = self.tail = node
            node.next = node
        else:
            node.next = self.head
            self.tail.next = node
            self.head = node

        self.size += 1
        return node

    def insert_after(self, node, value):
        if node is None:
            raise ValueError("node cannot be None")

        new_node = CircularNode(value)
        new_node.next = node.next
        node.next = new_node

        if node is self.tail:
            self.tail = new_node

        self.size += 1
        return new_node

    def delete_value(self, value):
        if self.head is None:
            return False

        current = self.head
        prev = self.tail

        while True:
            if current.value == value:
                if self.size == 1:
                    self.head = self.tail = None
                else:
                    prev.next = current.next

                    if current is self.head:
                        self.head = current.next

                    if current is self.tail:
                        self.tail = prev

                self.size -= 1
                return True

            prev = current
            current = current.next

            if current is self.head:
                break

        return False

    def search(self, value):
        if self.head is None:
            return None

        current = self.head

        while True:
            if current.value == value:
                return current

            current = current.next

            if current is self.head:
                break

        return None


# ============================================================
# 4. GENERIC SINGLY LINKED LIST FUNCTIONS
# ============================================================

def reverse_nodes(head):
    """Reverse a singly linked list and return new head."""
    prev = None
    current = head

    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt

    return prev


def reverse_nodes_recursive(head):
    if head is None or head.next is None:
        return head

    new_head = reverse_nodes_recursive(head.next)

    head.next.next = head
    head.next = None

    return new_head


def get_middle(head):
    """Returns second middle for even-sized list."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def get_first_middle(head):
    """Returns first middle for even-sized list."""
    slow = fast = head

    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def nth_from_end(head, n):
    if n <= 0:
        raise ValueError("n must be positive")

    fast = slow = head

    for _ in range(n):
        if fast is None:
            return None
        fast = fast.next

    while fast:
        slow = slow.next
        fast = fast.next

    return slow


# ============================================================
# 5. FAST / SLOW POINTER PATTERNS
# ============================================================

def detect_cycle(head):
    """Floyd's cycle detection / tortoise and hare."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False


def find_cycle_entry(head):
    """Returns cycle entry node or None."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            slow = head

            while slow is not fast:
                slow = slow.next
                fast = fast.next

            return slow

    return None


def cycle_length(head):
    meeting = get_cycle_meeting_node(head)

    if meeting is None:
        return 0

    length = 1
    current = meeting.next

    while current is not meeting:
        current = current.next
        length += 1

    return length


def get_cycle_meeting_node(head):
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return slow

    return None


def remove_cycle(head):
    entry = find_cycle_entry(head)

    if entry is None:
        return False

    current = entry

    while current.next is not entry:
        current = current.next

    current.next = None
    return True


# ============================================================
# 6. MERGING LINKED LISTS
# ============================================================

def merge_two_sorted_lists(l1, l2):
    """Iterative merge of two sorted singly linked lists."""
    dummy = SinglyNode(0)
    current = dummy

    while l1 and l2:
        if l1.value <= l2.value:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next

        current = current.next

    current.next = l1 if l1 else l2

    return dummy.next


def merge_two_sorted_lists_recursive(l1, l2):
    if l1 is None:
        return l2

    if l2 is None:
        return l1

    if l1.value <= l2.value:
        l1.next = merge_two_sorted_lists_recursive(l1.next, l2)
        return l1

    l2.next = merge_two_sorted_lists_recursive(l1, l2.next)
    return l2


def merge_k_sorted_lists(lists):
    """
    Divide-and-conquer merge.
    O(N log k), where N = total nodes.
    """
    if not lists:
        return None

    current = lists

    while len(current) > 1:
        merged = []

        for i in range(0, len(current), 2):
            l1 = current[i]
            l2 = current[i + 1] if i + 1 < len(current) else None
            merged.append(merge_two_sorted_lists(l1, l2))

        current = merged

    return current[0]


# ============================================================
# 7. INTERSECTION OF TWO LINKED LISTS
# ============================================================

def get_intersection_node(head_a, head_b):
    """
    Elegant two-pointer solution.

    Pointer A traverses:
        A -> ... -> common -> ... -> None -> B

    Pointer B traverses:
        B -> ... -> common -> ... -> None -> A

    They travel the same total distance.
    """
    a = head_a
    b = head_b

    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a

    return a


# ============================================================
# 8. PALINDROME LINKED LIST
# ============================================================

def is_palindrome(head):
    if head is None or head.next is None:
        return True

    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second_half = reverse_nodes(slow)

    first = head
    second = second_half

    result = True

    while second:
        if first.value != second.value:
            result = False
            break

        first = first.next
        second = second.next

    # Restore original structure.
    reverse_nodes(second_half)

    return result


# ============================================================
# 9. ROTATE LINKED LIST
# ============================================================

def rotate_right(head, k):
    if head is None or head.next is None or k == 0:
        return head

    length = 1
    tail = head

    while tail.next:
        tail = tail.next
        length += 1

    k %= length

    if k == 0:
        return head

    tail.next = head

    steps = length - k
    new_tail = head

    for _ in range(steps - 1):
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None

    return new_head


# ============================================================
# 10. REORDER LIST
# ============================================================

def reorder_list(head):
    """
    L0 -> L1 -> L2 -> ... -> Ln
    becomes
    L0 -> Ln -> L1 -> Ln-1 -> ...
    """
    if head is None or head.next is None:
        return head

    slow = fast = head

    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    second = slow.next
    slow.next = None

    second = reverse_nodes(second)

    first = head

    while second:
        first_next = first.next
        second_next = second.next

        first.next = second
        second.next = first_next

        first = first_next
        second = second_next

    return head


# ============================================================
# 11. SORT A LINKED LIST — MERGE SORT
# ============================================================

def merge_sort_nodes(head):
    if head is None or head.next is None:
        return head

    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    right = slow.next
    slow.next = None

    left = merge_sort_nodes(head)
    right = merge_sort_nodes(right)

    return merge_two_sorted_lists(left, right)


def sort_linked_list(head):
    return merge_sort_nodes(head)


# ============================================================
# 12. REMOVE DUPLICATES
# ============================================================

def remove_duplicates_sorted(head):
    current = head

    while current and current.next:
        if current.value == current.next.value:
            current.next = current.next.next
        else:
            current = current.next

    return head


def remove_duplicates_unsorted_with_set(head):
    seen = set()
    current = head
    prev = None

    while current:
        if current.value in seen:
            prev.next = current.next
        else:
            seen.add(current.value)
            prev = current

        current = current.next

    return head


def remove_all_duplicates_sorted(head):
    """
    For sorted list:
    1 -> 1 -> 2 -> 3 -> 3
    becomes:
    2
    """
    dummy = SinglyNode(0)
    dummy.next = head

    prev = dummy
    current = head

    while current:
        duplicate = False

        while current.next and current.value == current.next.value:
            duplicate = True
            current = current.next

        if duplicate:
            prev.next = current.next
        else:
            prev = prev.next

        current = current.next

    return dummy.next


# ============================================================
# 13. SWAP NODES IN PAIRS
# ============================================================

def swap_pairs(head):
    dummy = SinglyNode(0)
    dummy.next = head

    prev = dummy

    while prev.next and prev.next.next:
        first = prev.next
        second = first.next

        first.next = second.next
        second.next = first
        prev.next = second

        prev = first

    return dummy.next


# ============================================================
# 14. REVERSE NODES IN K-GROUPS
# ============================================================

def reverse_k_group(head, k):
    if k <= 1 or head is None:
        return head

    dummy = SinglyNode(0)
    dummy.next = head

    group_prev = dummy

    while True:
        kth = get_kth_node(group_prev, k)

        if kth is None:
            break

        group_next = kth.next

        prev = group_next
        current = group_prev.next

        while current is not group_next:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        old_start = group_prev.next
        group_prev.next = kth
        group_prev = old_start

    return dummy.next


def get_kth_node(start, k):
    current = start

    for _ in range(k):
        current = current.next

        if current is None:
            return None

    return current


# ============================================================
# 15. DELETE NODE GIVEN ONLY THAT NODE
# ============================================================

def delete_given_node(node):
    """
    Works only when node is NOT the tail.
    """
    if node is None or node.next is None:
        raise ValueError("Cannot delete the tail using this method")

    node.value = node.next.value
    node.next = node.next.next


# ============================================================
# 16. ADD TWO NUMBERS REPRESENTED BY LINKED LISTS
# ============================================================

def add_two_numbers(l1, l2):
    """
    Digits are stored in reverse order.

    Example:
    2 -> 4 -> 3
    5 -> 6 -> 4
    = 7 -> 0 -> 8
    """
    dummy = SinglyNode(0)
    current = dummy
    carry = 0

    while l1 or l2 or carry:
        x = l1.value if l1 else 0
        y = l2.value if l2 else 0

        total = x + y + carry
        carry = total // 10

        current.next = SinglyNode(total % 10)
        current = current.next

        if l1:
            l1 = l1.next

        if l2:
            l2 = l2.next

    return dummy.next


# ============================================================
# 17. PARTITION LIST
# ============================================================

def partition_list(head, x):
    before_dummy = SinglyNode(0)
    after_dummy = SinglyNode(0)

    before = before_dummy
    after = after_dummy

    current = head

    while current:
        if current.value < x:
            before.next = current
            before = before.next
        else:
            after.next = current
            after = after.next

        current = current.next

    after.next = None
    before.next = after_dummy.next

    return before_dummy.next


# ============================================================
# 18. ODD-EVEN LINKED LIST
# ============================================================

def odd_even_list(head):
    if head is None or head.next is None:
        return head

    odd = head
    even = head.next
    even_head = even

    while even and even.next:
        odd.next = even.next
        odd = odd.next

        even.next = odd.next
        even = even.next

    odd.next = even_head

    return head


# ============================================================
# 19. REMOVE ZERO-SUM CONSECUTIVE NODES
# ============================================================

def remove_zero_sum_sublists(head):
    """
    Prefix-sum + hashmap pattern.
    """
    dummy = SinglyNode(0)
    dummy.next = head

    prefix = 0
    seen = {}

    current = dummy

    while current:
        prefix += current.value
        seen[prefix] = current
        current = current.next

    prefix = 0
    current = dummy

    while current:
        prefix += current.value

        if prefix in seen:
            current.next = seen[prefix].next

        current = current.next

    return dummy.next


# ============================================================
# 20. COPY LIST WITH RANDOM POINTER
# ============================================================

class RandomNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.random = None


def copy_random_list(head):
    """
    HashMap solution.

    Original node -> copied node
    """
    if head is None:
        return None

    mapping = {}

    current = head

    while current:
        mapping[current] = RandomNode(current.value)
        current = current.next

    current = head

    while current:
        copy = mapping[current]
        copy.next = mapping.get(current.next)
        copy.random = mapping.get(current.random)
        current = current.next

    return mapping[head]


# ============================================================
# 21. FLATTEN MULTILEVEL DOUBLY LINKED LIST
# ============================================================

class MultiLevelNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
        self.child = None


def flatten_multilevel_doubly_list(head):
    if head is None:
        return None

    stack = [head]
    prev = None

    while stack:
        current = stack.pop()

        if prev:
            prev.next = current
            current.prev = prev

        if current.next:
            stack.append(current.next)

        if current.child:
            stack.append(current.child)
            current.child = None

        prev = current

    return head


# ============================================================
# 22. LRU CACHE BUILDING BLOCK
# ============================================================

class LRUNode:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    Classic interview design:
        HashMap + Doubly Linked List

    get  -> O(1)
    put  -> O(1)
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self.capacity = capacity
        self.cache = {}

        self.left = LRUNode()   # least recently used sentinel
        self.right = LRUNode()  # most recently used sentinel

        self.left.next = self.right
        self.right.prev = self.left

    def _remove(self, node):
        prev = node.prev
        nxt = node.next

        prev.next = nxt
        nxt.prev = prev

    def _insert_right(self, node):
        prev = self.right.prev

        prev.next = node
        node.prev = prev

        node.next = self.right
        self.right.prev = node

    def get(self, key):
        if key not in self.cache:
            return -1

        node = self.cache[key]

        self._remove(node)
        self._insert_right(node)

        return node.value

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])

        node = LRUNode(key, value)
        self.cache[key] = node
        self._insert_right(node)

        if len(self.cache) > self.capacity:
            lru = self.left.next
            self._remove(lru)
            del self.cache[lru.key]


# ============================================================
# 23. USEFUL CONSTRUCTION HELPERS
# ============================================================

def build_singly(values):
    """Build and return head only."""
    dummy = SinglyNode(0)
    current = dummy

    for value in values:
        current.next = SinglyNode(value)
        current = current.next

    return dummy.next


def list_from_head(head, limit=100):
    """
    Safe conversion for revision/debugging.
    limit prevents infinite loops on cyclic lists.
    """
    result = []
    current = head
    count = 0

    while current and count < limit:
        result.append(current.value)
        current = current.next
        count += 1

    if current is not None:
        result.append("...cycle...")

    return result


def create_cycle(head, position):
    """
    position = 0-based index of node where tail should point.
    """
    if head is None:
        return head

    cycle_node = None
    current = head
    index = 0
    tail = None

    while current:
        if index == position:
            cycle_node = current

        tail = current
        current = current.next
        index += 1

    if cycle_node is None:
        raise IndexError("Invalid cycle position")

    tail.next = cycle_node

    return head


# ============================================================
# 24. INTERVIEW-STYLE TESTS
# ============================================================

def run_revision_tests():
    # Singly Linked List
    ll = SinglyLinkedList([1, 2, 3, 4, 5])

    assert ll.to_list() == [1, 2, 3, 4, 5]
    assert ll.get(2) == 3
    assert ll.find(4) == 3

    ll.prepend(0)
    ll.append(6)
    ll.insert_at(3, 99)

    assert ll.to_list() == [0, 1, 2, 99, 3, 4, 5, 6]

    ll.delete_value(99)
    assert ll.to_list() == [0, 1, 2, 3, 4, 5, 6]

    assert ll.middle_node().value == 3
    assert ll.nth_from_end(1).value == 6

    ll.reverse_iterative()
    assert ll.to_list() == [6, 5, 4, 3, 2, 1, 0]

    ll.reverse_recursive()
    assert ll.to_list() == [0, 1, 2, 3, 4, 5, 6]

    # Palindrome
    palindrome = build_singly([1, 2, 3, 2, 1])
    assert is_palindrome(palindrome)

    # Merge
    a = build_singly([1, 3, 5])
    b = build_singly([2, 4, 6])

    merged = merge_two_sorted_lists(a, b)
    assert list_from_head(merged) == [1, 2, 3, 4, 5, 6]

    # Cycle
    cyclic = build_singly([1, 2, 3, 4, 5])
    create_cycle(cyclic, 2)

    assert detect_cycle(cyclic)
    assert find_cycle_entry(cyclic).value == 3
    assert cycle_length(cyclic) == 3

    remove_cycle(cyclic)

    assert not detect_cycle(cyclic)

    # Doubly
    dll = DoublyLinkedList([1, 2, 3])
    assert dll.to_list() == [1, 2, 3]
    assert dll.to_reverse_list() == [3, 2, 1]

    dll.reverse()
    assert dll.to_list() == [3, 2, 1]

    # Circular
    cll = CircularLinkedList([1, 2, 3])
    assert cll.to_list() == [1, 2, 3]

    # K-group
    kg = build_singly([1, 2, 3, 4, 5])
    kg = reverse_k_group(kg, 2)

    assert list_from_head(kg) == [2, 1, 4, 3, 5]

    # Swap pairs
    sp = build_singly([1, 2, 3, 4])
    sp = swap_pairs(sp)

    assert list_from_head(sp) == [2, 1, 4, 3]

    print("All Linked List revision tests passed! ✓")


# ============================================================
# 25. PLACEMENT REVISION CHECKLIST
# ============================================================

"""
BEFORE PLACEMENTS, YOU SHOULD BE ABLE TO CODE THESE WITHOUT LOOKING:

BASIC
[ ] Create node
[ ] Create linked list
[ ] Traverse
[ ] Search
[ ] Insert at head
[ ] Insert at tail
[ ] Insert at position
[ ] Delete head
[ ] Delete tail
[ ] Delete by value
[ ] Delete by position
[ ] Update node

POINTER FUNDAMENTALS
[ ] Reverse iteratively
[ ] Reverse recursively
[ ] Find middle
[ ] Find nth node from end
[ ] Remove nth node from end
[ ] Fast/slow pointer

CYCLE
[ ] Detect cycle
[ ] Find cycle entry
[ ] Find cycle length
[ ] Remove cycle

CORE INTERVIEW
[ ] Merge two sorted lists
[ ] Merge K sorted lists
[ ] Check palindrome
[ ] Intersection of two lists
[ ] Remove duplicates
[ ] Rotate list
[ ] Reorder list
[ ] Sort linked list

ADVANCED
[ ] Swap nodes in pairs
[ ] Reverse nodes in K-group
[ ] Partition list
[ ] Odd-even list
[ ] Add two numbers
[ ] Remove zero-sum sublists
[ ] Copy random-pointer list
[ ] Flatten multilevel doubly list
[ ] LRU Cache

DOUBLY
[ ] Insert before
[ ] Insert after
[ ] Delete known node
[ ] Reverse DLL

CIRCULAR
[ ] Create circular list
[ ] Traverse safely
[ ] Insert
[ ] Delete
[ ] Search

INTERVIEW QUESTIONS TO EXPLAIN
[ ] Why is linked-list access O(n)?
[ ] Why is insertion at head O(1)?
[ ] Why is deletion of a known DLL node O(1)?
[ ] Why does Floyd cycle detection work?
[ ] Why does fast move 2x slow?
[ ] How do you find cycle entry?
[ ] How do you find the middle in one pass?
[ ] How do you reverse a list in O(1) extra space?
[ ] Why is merge sort preferred for linked lists?
[ ] Why is random access poor?
[ ] Array vs Linked List?
[ ] Singly vs Doubly?
[ ] Circular vs Linear?
[ ] HashMap + DLL for LRU Cache?
"""


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LINKED LIST — COMPLETE REVISION LIBRARY")
    print("=" * 60)
    print()
    print("Singly Linked List   ✓")
    print("Doubly Linked List   ✓")
    print("Circular Linked List ✓")
    print("Fast / Slow Pointers ✓")
    print("Cycle Algorithms     ✓")
    print("Merge Algorithms     ✓")
    print("Advanced Patterns   ✓")
    print()
    print("Run run_revision_tests() to verify the implementations.")
    print("=" * 60)

    # Uncomment to run:
    # run_revision_tests()

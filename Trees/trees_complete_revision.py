"""
TREES — COMPLETE DSA REVISION
=============================

Placement revision library for:
- Binary Trees
- Binary Search Trees (BST)
- Heaps / Priority Queues
- Tries
- Tree traversals
- Recursive tree patterns
- DFS / BFS
- Height / Diameter
- Balanced trees
- Lowest Common Ancestor
- Path problems
- Views
- Serialization
- BST operations
- Heap operations
- Trie operations

Use this file for revision before interviews.
"""

from collections import deque
import heapq


# ============================================================
# BINARY TREE NODE
# ============================================================

class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# ============================================================
# TREE CREATION / HELPERS
# ============================================================

def build_tree_level_order(values):
    """Build a binary tree from level-order values.
    Use None for missing nodes.
    """
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def tree_to_level_order(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()

        if node is None:
            result.append(None)
            continue

        result.append(node.value)
        queue.append(node.left)
        queue.append(node.right)

    while result and result[-1] is None:
        result.pop()

    return result


# ============================================================
# DFS — RECURSIVE TRAVERSALS
# ============================================================

def preorder_recursive(root):
    """Root -> Left -> Right"""
    result = []

    def dfs(node):
        if node is None:
            return

        result.append(node.value)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def inorder_recursive(root):
    """Left -> Root -> Right"""
    result = []

    def dfs(node):
        if node is None:
            return

        dfs(node.left)
        result.append(node.value)
        dfs(node.right)

    dfs(root)
    return result


def postorder_recursive(root):
    """Left -> Right -> Root"""
    result = []

    def dfs(node):
        if node is None:
            return

        dfs(node.left)
        dfs(node.right)
        result.append(node.value)

    dfs(root)
    return result


# ============================================================
# DFS — ITERATIVE TRAVERSALS
# ============================================================

def preorder_iterative(root):
    if root is None:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.value)

        if node.right:
            stack.append(node.right)

        if node.left:
            stack.append(node.left)

    return result


def inorder_iterative(root):
    result = []
    stack = []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        result.append(current.value)
        current = current.right

    return result


def postorder_iterative_two_stacks(root):
    if root is None:
        return []

    stack1 = [root]
    stack2 = []
    result = []

    while stack1:
        node = stack1.pop()
        stack2.append(node)

        if node.left:
            stack1.append(node.left)

        if node.right:
            stack1.append(node.right)

    while stack2:
        result.append(stack2.pop().value)

    return result


def postorder_iterative_one_stack(root):
    result = []
    stack = []
    current = root
    last_visited = None

    while current or stack:
        if current:
            stack.append(current)
            current = current.left
        else:
            peek = stack[-1]

            if peek.right and last_visited is not peek.right:
                current = peek.right
            else:
                result.append(peek.value)
                last_visited = stack.pop()

    return result


# ============================================================
# MORRIS TRAVERSALS — O(1) EXTRA SPACE
# ============================================================

def morris_inorder(root):
    result = []
    current = root

    while current:
        if current.left is None:
            result.append(current.value)
            current = current.right
        else:
            predecessor = current.left

            while predecessor.right and predecessor.right is not current:
                predecessor = predecessor.right

            if predecessor.right is None:
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                result.append(current.value)
                current = current.right

    return result


def morris_preorder(root):
    result = []
    current = root

    while current:
        if current.left is None:
            result.append(current.value)
            current = current.right
        else:
            predecessor = current.left

            while predecessor.right and predecessor.right is not current:
                predecessor = predecessor.right

            if predecessor.right is None:
                result.append(current.value)
                predecessor.right = current
                current = current.left
            else:
                predecessor.right = None
                current = current.right

    return result


# ============================================================
# BFS / LEVEL ORDER
# ============================================================

def level_order(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []

        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.value)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


def level_order_flat(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.value)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return result


def reverse_level_order(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.value)

        if node.right:
            queue.append(node.right)

        if node.left:
            queue.append(node.left)

    return result[::-1]


# ============================================================
# BASIC TREE PROPERTIES
# ============================================================

def max_depth(root):
    if root is None:
        return 0

    return 1 + max(max_depth(root.left), max_depth(root.right))


def min_depth(root):
    if root is None:
        return 0

    queue = deque([(root, 1)])

    while queue:
        node, depth = queue.popleft()

        if node.left is None and node.right is None:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))

        if node.right:
            queue.append((node.right, depth + 1))

    return 0


def count_nodes(root):
    if root is None:
        return 0

    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root):
    if root is None:
        return 0

    if root.left is None and root.right is None:
        return 1

    return count_leaves(root.left) + count_leaves(root.right)


def sum_tree(root):
    if root is None:
        return 0

    return root.value + sum_tree(root.left) + sum_tree(root.right)


def maximum_value(root):
    if root is None:
        raise ValueError("Tree is empty")

    return max(
        root.value,
        maximum_value(root.left) if root.left else float("-inf"),
        maximum_value(root.right) if root.right else float("-inf")
    )


# ============================================================
# TREE COMPARISON
# ============================================================

def is_same_tree(p, q):
    if p is None and q is None:
        return True

    if p is None or q is None:
        return False

    return (
        p.value == q.value
        and is_same_tree(p.left, q.left)
        and is_same_tree(p.right, q.right)
    )


def is_symmetric(root):
    def mirror(a, b):
        if a is None and b is None:
            return True

        if a is None or b is None:
            return False

        return (
            a.value == b.value
            and mirror(a.left, b.right)
            and mirror(a.right, b.left)
        )

    return True if root is None else mirror(root.left, root.right)


def is_subtree(root, subroot):
    if subroot is None:
        return True

    if root is None:
        return False

    if is_same_tree(root, subroot):
        return True

    return is_subtree(root.left, subroot) or is_subtree(root.right, subroot)


# ============================================================
# BALANCED TREE / DIAMETER
# ============================================================

def is_balanced(root):
    def height(node):
        if node is None:
            return 0

        left = height(node.left)
        if left == -1:
            return -1

        right = height(node.right)
        if right == -1:
            return -1

        if abs(left - right) > 1:
            return -1

        return 1 + max(left, right)

    return height(root) != -1


def diameter_of_tree(root):
    diameter = 0

    def height(node):
        nonlocal diameter

        if node is None:
            return 0

        left = height(node.left)
        right = height(node.right)

        diameter = max(diameter, left + right)

        return 1 + max(left, right)

    height(root)
    return diameter


# ============================================================
# PATH PROBLEMS
# ============================================================

def has_path_sum(root, target):
    if root is None:
        return False

    if root.left is None and root.right is None:
        return root.value == target

    remaining = target - root.value

    return (
        has_path_sum(root.left, remaining)
        or has_path_sum(root.right, remaining)
    )


def all_root_to_leaf_paths(root):
    result = []

    def dfs(node, path):
        if node is None:
            return

        path.append(node.value)

        if node.left is None and node.right is None:
            result.append(path[:])
        else:
            dfs(node.left, path)
            dfs(node.right, path)

        path.pop()

    dfs(root, [])
    return result


def max_path_sum(root):
    best = float("-inf")

    def dfs(node):
        nonlocal best

        if node is None:
            return 0

        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        best = max(best, node.value + left + right)

        return node.value + max(left, right)

    dfs(root)
    return best


def sum_numbers_from_root_to_leaf(root):
    def dfs(node, current):
        if node is None:
            return 0

        current = current * 10 + node.value

        if node.left is None and node.right is None:
            return current

        return dfs(node.left, current) + dfs(node.right, current)

    return dfs(root, 0)


# ============================================================
# LOWEST COMMON ANCESTOR
# ============================================================

def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root

    return left if left else right


def lowest_common_ancestor_by_value(root, p_value, q_value):
    def lca(node):
        if node is None:
            return None

        if node.value == p_value or node.value == q_value:
            return node

        left = lca(node.left)
        right = lca(node.right)

        if left and right:
            return node

        return left or right

    return lca(root)


# ============================================================
# TREE VIEWS
# ============================================================

def right_side_view(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)

        for i in range(level_size):
            node = queue.popleft()

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

            if i == level_size - 1:
                result.append(node.value)

    return result


def left_side_view(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)

        for i in range(level_size):
            node = queue.popleft()

            if i == 0:
                result.append(node.value)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

    return result


def top_view(root):
    if root is None:
        return []

    result = {}
    queue = deque([(root, 0)])

    while queue:
        node, column = queue.popleft()

        if column not in result:
            result[column] = node.value

        if node.left:
            queue.append((node.left, column - 1))

        if node.right:
            queue.append((node.right, column + 1))

    return [result[c] for c in sorted(result)]


def bottom_view(root):
    if root is None:
        return []

    result = {}
    queue = deque([(root, 0)])

    while queue:
        node, column = queue.popleft()
        result[column] = node.value

        if node.left:
            queue.append((node.left, column - 1))

        if node.right:
            queue.append((node.right, column + 1))

    return [result[c] for c in sorted(result)]


# ============================================================
# ZIGZAG / SPIRAL LEVEL ORDER
# ============================================================

def zigzag_level_order(root):
    if root is None:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level = [0] * len(queue)

        for i in range(len(queue)):
            node = queue.popleft()

            index = i if left_to_right else len(level) - 1 - i
            level[index] = node.value

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        result.append(level)
        left_to_right = not left_to_right

    return result


# ============================================================
# BURNING TREE
# ============================================================

def burning_tree_time(root, target):
    """Returns time required to burn the whole tree."""
    if root is None:
        return -1

    parent = {}
    target_node = None
    queue = deque([root])

    while queue:
        node = queue.popleft()

        if node.value == target:
            target_node = node

        if node.left:
            parent[node.left] = node
            queue.append(node.left)

        if node.right:
            parent[node.right] = node
            queue.append(node.right)

    if target_node is None:
        return -1

    visited = {target_node}
    queue = deque([target_node])
    time = -1

    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()

            neighbors = [
                node.left,
                node.right,
                parent.get(node)
            ]

            for neighbor in neighbors:
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        time += 1

    return time


# ============================================================
# SERIALIZATION / DESERIALIZATION
# ============================================================

def serialize(root):
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()

        if node is None:
            result.append(None)
            continue

        result.append(node.value)
        queue.append(node.left)
        queue.append(node.right)

    return result


def deserialize(values):
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


# ============================================================
# CONSTRUCT TREE FROM TRAVERSALS
# ============================================================

def build_from_preorder_inorder(preorder, inorder):
    if not preorder:
        return None

    positions = {value: i for i, value in enumerate(inorder)}
    pre_index = 0

    def build(left, right):
        nonlocal pre_index

        if left > right:
            return None

        value = preorder[pre_index]
        pre_index += 1

        root = TreeNode(value)
        mid = positions[value]

        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)

        return root

    return build(0, len(inorder) - 1)


def build_from_inorder_postorder(inorder, postorder):
    if not inorder:
        return None

    positions = {value: i for i, value in enumerate(inorder)}
    post_index = len(postorder) - 1

    def build(left, right):
        nonlocal post_index

        if left > right:
            return None

        value = postorder[post_index]
        post_index -= 1

        root = TreeNode(value)
        mid = positions[value]

        root.right = build(mid + 1, right)
        root.left = build(left, mid - 1)

        return root

    return build(0, len(inorder) - 1)


# ============================================================
# BST NODE / OPERATIONS
# ============================================================

def bst_search(root, target):
    current = root

    while current:
        if current.value == target:
            return current

        if target < current.value:
            current = current.left
        else:
            current = current.right

    return None


def bst_insert(root, value):
    if root is None:
        return TreeNode(value)

    if value < root.value:
        root.left = bst_insert(root.left, value)
    elif value > root.value:
        root.right = bst_insert(root.right, value)

    return root


def bst_insert_iterative(root, value):
    new_node = TreeNode(value)

    if root is None:
        return new_node

    current = root

    while True:
        if value < current.value:
            if current.left is None:
                current.left = new_node
                break
            current = current.left

        elif value > current.value:
            if current.right is None:
                current.right = new_node
                break
            current = current.right

        else:
            break

    return root


def bst_min(root):
    if root is None:
        return None

    current = root

    while current.left:
        current = current.left

    return current


def bst_max(root):
    if root is None:
        return None

    current = root

    while current.right:
        current = current.right

    return current


def bst_successor(root, target):
    successor = None
    current = root

    while current:
        if target < current.value:
            successor = current
            current = current.left
        else:
            current = current.right

    return successor


def bst_predecessor(root, target):
    predecessor = None
    current = root

    while current:
        if target > current.value:
            predecessor = current
            current = current.right
        else:
            current = current.left

    return predecessor


def bst_delete(root, key):
    if root is None:
        return None

    if key < root.value:
        root.left = bst_delete(root.left, key)

    elif key > root.value:
        root.right = bst_delete(root.right, key)

    else:
        # Case 1 / 2: zero or one child.
        if root.left is None:
            return root.right

        if root.right is None:
            return root.left

        # Case 3: two children.
        successor = bst_min(root.right)
        root.value = successor.value
        root.right = bst_delete(root.right, successor.value)

    return root


def is_valid_bst(root):
    def validate(node, low, high):
        if node is None:
            return True

        if not (low < node.value < high):
            return False

        return (
            validate(node.left, low, node.value)
            and validate(node.right, node.value, high)
        )

    return validate(root, float("-inf"), float("inf"))


def kth_smallest_bst(root, k):
    stack = []
    current = root
    count = 0

    while current or stack:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        count += 1

        if count == k:
            return current.value

        current = current.right

    return None


def kth_largest_bst(root, k):
    stack = []
    current = root
    count = 0

    while current or stack:
        while current:
            stack.append(current)
            current = current.right

        current = stack.pop()
        count += 1

        if count == k:
            return current.value

        current = current.left

    return None


def bst_lca(root, p, q):
    current = root

    while current:
        if p < current.value and q < current.value:
            current = current.left
        elif p > current.value and q > current.value:
            current = current.right
        else:
            return current

    return None


# ============================================================
# BST FROM SORTED ARRAY
# ============================================================

def sorted_array_to_bst(nums):
    if not nums:
        return None

    mid = len(nums) // 2
    root = TreeNode(nums[mid])

    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid + 1:])

    return root


# ============================================================
# HEAPS / PRIORITY QUEUE
# ============================================================

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, value)

    def pop(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return heapq.heappop(self.heap)

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def size(self):
        return len(self.heap)


class MaxHeap:
    """Python heapq is a min-heap, so store negative values."""

    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, -value)

    def pop(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return -heapq.heappop(self.heap)

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty")
        return -self.heap[0]

    def size(self):
        return len(self.heap)


def heapify_min(nums):
    heap = nums[:]
    heapq.heapify(heap)
    return heap


def kth_largest_heap(nums, k):
    heap = []

    for value in nums:
        heapq.heappush(heap, value)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


def kth_smallest_heap(nums, k):
    return heapq.nsmallest(k, nums)[-1]


def top_k_frequent(nums, k):
    frequency = {}

    for value in nums:
        frequency[value] = frequency.get(value, 0) + 1

    heap = []

    for value, freq in frequency.items():
        heapq.heappush(heap, (freq, value))

        if len(heap) > k:
            heapq.heappop(heap)

    return [value for _, value in heap]


def merge_k_sorted_arrays(arrays):
    heap = []
    result = []

    for array_index, array in enumerate(arrays):
        if array:
            heapq.heappush(heap, (array[0], array_index, 0))

    while heap:
        value, array_index, element_index = heapq.heappop(heap)
        result.append(value)

        next_index = element_index + 1

        if next_index < len(arrays[array_index]):
            next_value = arrays[array_index][next_index]
            heapq.heappush(
                heap,
                (next_value, array_index, next_index)
            )

    return result


def kth_smallest_in_sorted_matrix(matrix, k):
    heap = []
    n = len(matrix)

    for row in range(min(n, k)):
        if matrix[row]:
            heapq.heappush(heap, (matrix[row][0], row, 0))

    value = None

    for _ in range(k):
        value, row, col = heapq.heappop(heap)

        if col + 1 < len(matrix[row]):
            heapq.heappush(
                heap,
                (matrix[row][col + 1], row, col + 1)
            )

    return value


# ============================================================
# TRIE
# ============================================================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root

        for ch in word:
            if ch not in current.children:
                current.children[ch] = TrieNode()

            current = current.children[ch]

        current.is_end = True

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find_node(prefix) is not None

    def _find_node(self, text):
        current = self.root

        for ch in text:
            if ch not in current.children:
                return None

            current = current.children[ch]

        return current

    def delete(self, word):
        def remove(node, index):
            if index == len(word):
                if not node.is_end:
                    return False

                node.is_end = False
                return len(node.children) == 0

            ch = word[index]

            if ch not in node.children:
                return False

            should_delete_child = remove(
                node.children[ch],
                index + 1
            )

            if should_delete_child:
                del node.children[ch]

            return (
                not node.is_end
                and len(node.children) == 0
            )

        remove(self.root, 0)

    def words_with_prefix(self, prefix):
        node = self._find_node(prefix)

        if node is None:
            return []

        result = []

        def dfs(current, path):
            if current.is_end:
                result.append(prefix + "".join(path))

            for ch in sorted(current.children):
                path.append(ch)
                dfs(current.children[ch], path)
                path.pop()

        dfs(node, [])
        return result


def replace_words_with_trie(dictionary, sentence):
    trie = Trie()

    for word in dictionary:
        trie.insert(word)

    result = []

    for word in sentence.split():
        current = trie.root
        prefix = None

        for i, ch in enumerate(word):
            if ch not in current.children:
                break

            current = current.children[ch]

            if current.is_end:
                prefix = word[:i + 1]
                break

        result.append(prefix if prefix else word)

    return " ".join(result)


# ============================================================
# TREE ALGORITHM PATTERNS
# ============================================================

def recursive_tree_template(root):
    """
    Generic tree recursion:

    def dfs(node):
        if node is None:
            return base_value

        left = dfs(node.left)
        right = dfs(node.right)

        return combine(node, left, right)

    Always identify:
        1. Base case
        2. Information returned from left
        3. Information returned from right
        4. How current node combines them
    """
    raise NotImplementedError


def tree_bfs_template(root):
    """
    Generic BFS:

    queue = deque([root])

    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)
    """
    raise NotImplementedError


# ============================================================
# INTERVIEW CHEAT SHEET
# ============================================================

"""
TREE PATTERN RECOGNITION
========================

1. Need traversal?
   -> DFS / BFS

2. Need level-by-level answer?
   -> BFS

3. Need path / subtree information?
   -> DFS recursion

4. Need shortest distance in an unweighted tree?
   -> BFS

5. Need height?
   -> 1 + max(left, right)

6. Need diameter?
   -> left height + right height

7. Need balance?
   -> return height, use -1 as invalid marker

8. Need root-to-leaf path?
   -> DFS + backtracking/path

9. Need all paths?
   -> DFS + path.append / path.pop

10. Need ancestor?
    -> LCA

11. BST?
    -> exploit ordering

12. kth smallest in BST?
    -> inorder

13. kth largest in BST?
    -> reverse inorder

14. Need top/bottom/side view?
    -> BFS + positional information

15. Need autocomplete?
    -> Trie

16. Need repeated minimum/maximum?
    -> Heap

17. Need merge K sorted structures?
    -> Min heap

18. Need Kth largest?
    -> Min heap of size K

19. Need Kth smallest?
    -> Max heap of size K or min-heap techniques


TREE COMPLEXITIES
================

Traversal:
    Time:  O(n)
    Space: O(h) recursion / stack

BFS:
    Time:  O(n)
    Space: O(w)

Height:
    Time:  O(n)

Diameter:
    Time:  O(n) with optimized DFS

Balanced check:
    Time:  O(n)

LCA:
    Time:  O(n) general binary tree
    Time:  O(h) BST

BST search:
    Average: O(log n)
    Worst:   O(n)

BST insert:
    Average: O(log n)
    Worst:   O(n)

BST delete:
    Average: O(log n)
    Worst:   O(n)

Heap push:
    O(log n)

Heap pop:
    O(log n)

Heap peek:
    O(1)

Trie insert/search:
    O(L)
    where L = word length


BST PROPERTY
============

For every node:

    all left values < node.value
    all right values > node.value

Therefore:

    inorder traversal of a valid BST
    produces sorted values.


TREE DFS ORDERS
===============

PREORDER:
    Root -> Left -> Right

INORDER:
    Left -> Root -> Right

POSTORDER:
    Left -> Right -> Root

Remember:

    PRE  = process root BEFORE children
    IN   = process root IN BETWEEN children
    POST = process root AFTER children


HEAP PROPERTY
=============

MIN HEAP:
    parent <= children

MAX HEAP:
    parent >= children

Important:
    A heap is NOT a BST.

Heap gives fast access to:
    minimum / maximum


TRIE
====

Insert:
    traverse/create characters

Search:
    traverse characters + check is_end

Prefix:
    traverse prefix

Autocomplete:
    find prefix node + DFS descendants


PLACEMENT CHECKLIST
===================

BINARY TREE
[ ] TreeNode
[ ] Build tree
[ ] Preorder recursive
[ ] Inorder recursive
[ ] Postorder recursive
[ ] Preorder iterative
[ ] Inorder iterative
[ ] Postorder iterative
[ ] Morris traversal
[ ] Level order
[ ] Reverse level order
[ ] Zigzag traversal
[ ] Height
[ ] Minimum depth
[ ] Count nodes
[ ] Count leaves
[ ] Same tree
[ ] Symmetric tree
[ ] Subtree
[ ] Balanced tree
[ ] Diameter
[ ] Path sum
[ ] Root-to-leaf paths
[ ] Maximum path sum
[ ] LCA
[ ] Right view
[ ] Left view
[ ] Top view
[ ] Bottom view
[ ] Serialize
[ ] Deserialize
[ ] Construct from traversals
[ ] Burning tree

BST
[ ] Search
[ ] Insert
[ ] Delete
[ ] Min / Max
[ ] Successor
[ ] Predecessor
[ ] Validate BST
[ ] Kth smallest
[ ] Kth largest
[ ] LCA in BST
[ ] Sorted array -> BST

HEAPS
[ ] Min heap
[ ] Max heap
[ ] Heapify
[ ] Kth largest
[ ] Kth smallest
[ ] Top K frequent
[ ] Merge K sorted arrays
[ ] Kth smallest matrix

TRIES
[ ] Trie node
[ ] Insert
[ ] Search
[ ] Prefix search
[ ] Delete
[ ] Autocomplete
[ ] Dictionary replacement


MOST IMPORTANT INTERVIEW QUESTIONS
==================================

1. Maximum Depth of Binary Tree
2. Same Tree
3. Invert Binary Tree
4. Symmetric Tree
5. Binary Tree Level Order Traversal
6. Zigzag Level Order Traversal
7. Diameter of Binary Tree
8. Balanced Binary Tree
9. Path Sum
10. Path Sum II
11. Lowest Common Ancestor
12. Binary Tree Maximum Path Sum
13. Serialize and Deserialize Binary Tree
14. Construct Tree from Preorder + Inorder
15. Construct Tree from Inorder + Postorder
16. Binary Tree Right Side View
17. Binary Tree Top View
18. Validate BST
19. Search in BST
20. Insert into BST
21. Delete Node in BST
22. Kth Smallest in BST
23. Lowest Common Ancestor of BST
24. Convert Sorted Array to BST
25. Kth Largest Element
26. Top K Frequent Elements
27. Merge K Sorted Arrays
28. Implement Trie
29. Word Search II concept
30. Autocomplete / Prefix Search


THE GOLDEN TREE RULE
====================

Before coding a tree problem, ask:

    "What information should my recursive function
     return to its parent?"

Examples:

Height:
    return height

Diameter:
    return height,
    update diameter globally

Balanced:
    return height or -1

LCA:
    return whether/where target was found

Maximum path sum:
    return best downward path,
    update global answer with both sides

This single question solves a huge fraction
of tree interview problems.
"""


# ============================================================
# TESTS
# ============================================================

def run_revision_tests():
    root = build_tree_level_order(
        [1, 2, 3, 4, 5, None, 7]
    )

    assert preorder_recursive(root) == [1, 2, 4, 5, 3, 7]
    assert inorder_recursive(root) == [4, 2, 5, 1, 3, 7]
    assert postorder_recursive(root) == [4, 5, 2, 7, 3, 1]

    assert preorder_iterative(root) == preorder_recursive(root)
    assert inorder_iterative(root) == inorder_recursive(root)
    assert postorder_iterative_two_stacks(root) == postorder_recursive(root)
    assert postorder_iterative_one_stack(root) == postorder_recursive(root)

    assert morris_inorder(root) == inorder_recursive(root)
    assert morris_preorder(root) == preorder_recursive(root)

    assert level_order(root) == [
        [1],
        [2, 3],
        [4, 5, 7]
    ]

    assert max_depth(root) == 3
    assert min_depth(root) == 3
    assert count_nodes(root) == 6
    assert count_leaves(root) == 3
    assert sum_tree(root) == 22
    assert maximum_value(root) == 7

    assert is_same_tree(root, build_tree_level_order(
        [1, 2, 3, 4, 5, None, 7]
    ))

    symmetric = build_tree_level_order(
        [1, 2, 2, 3, 4, 4, 3]
    )
    assert is_symmetric(symmetric)

    assert is_balanced(root)
    assert diameter_of_tree(root) == 4

    path_tree = build_tree_level_order(
        [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    )
    assert has_path_sum(path_tree, 22)
    assert max_path_sum(path_tree) == 48

    # LCA.
    p = root.left.left
    q = root.left.right
    assert lowest_common_ancestor(root, p, q).value == 2

    assert right_side_view(root) == [1, 3, 7]
    assert left_side_view(root) == [1, 2, 4]
    assert zigzag_level_order(root) == [
        [1], [3, 2], [4, 5, 7]
    ]

    serialized = serialize(root)
    rebuilt = deserialize(serialized)
    assert is_same_tree(root, rebuilt)

    constructed = build_from_preorder_inorder(
        [1, 2, 4, 5, 3, 7],
        [4, 2, 5, 1, 3, 7]
    )
    assert preorder_recursive(constructed) == [1, 2, 4, 5, 3, 7]

    # BST.
    bst = None
    for value in [5, 3, 7, 2, 4, 6, 8]:
        bst = bst_insert(bst, value)

    assert is_valid_bst(bst)
    assert bst_search(bst, 4).value == 4
    assert bst_min(bst).value == 2
    assert bst_max(bst).value == 8
    assert bst_successor(bst, 4).value == 5
    assert bst_predecessor(bst, 4).value == 3
    assert kth_smallest_bst(bst, 3) == 4
    assert kth_largest_bst(bst, 2) == 7
    assert bst_lca(bst, 2, 4).value == 3

    bst = bst_delete(bst, 3)
    assert is_valid_bst(bst)
    assert inorder_recursive(bst) == [2, 4, 5, 6, 7, 8]

    # Heaps.
    min_heap = MinHeap()
    for value in [5, 1, 8, 2]:
        min_heap.push(value)

    assert min_heap.peek() == 1
    assert min_heap.pop() == 1

    max_heap = MaxHeap()
    for value in [5, 1, 8, 2]:
        max_heap.push(value)

    assert max_heap.peek() == 8
    assert max_heap.pop() == 8

    assert kth_largest_heap(
        [3, 2, 1, 5, 6, 4], 2
    ) == 5

    assert merge_k_sorted_arrays([
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9]
    ]) == list(range(1, 10))

    # Trie.
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("apply")

    assert trie.search("apple")
    assert trie.search("app")
    assert not trie.search("ap")
    assert trie.starts_with("ap")
    assert sorted(trie.words_with_prefix("app")) == [
        "app", "apple", "apply"
    ]

    trie.delete("app")
    assert not trie.search("app")
    assert trie.search("apple")

    print("All Trees revision tests passed! ✓")


if __name__ == "__main__":
    print("=" * 70)
    print("TREES — COMPLETE DSA REVISION")
    print("=" * 70)
    print("Binary Tree fundamentals       ✓")
    print("DFS / BFS traversals           ✓")
    print("Recursive + iterative          ✓")
    print("Morris traversal               ✓")
    print("Tree properties                ✓")
    print("Diameter / balanced            ✓")
    print("Path problems                  ✓")
    print("LCA                            ✓")
    print("Tree views                     ✓")
    print("Serialization                  ✓")
    print("Tree construction              ✓")
    print("Binary Search Trees             ✓")
    print("BST operations                 ✓")
    print("Heaps / Priority Queues        ✓")
    print("Tries                          ✓")
    print("Interview cheat sheet          ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 70)

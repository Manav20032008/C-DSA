"""
QUEUE — COMPLETE REVISION FILE
==============================

Purpose:
    Single Python revision library for DSA / placement preparation.

Covers:
    1. Queue fundamentals
    2. Array/list based queue
    3. Circular queue
    4. Linked-list based queue
    5. Deque
    6. Priority Queue / Heap
    7. Queue using two stacks
    8. Stack using two queues
    9. BFS
    10. Level-order traversal
    11. Shortest path in unweighted graph
    12. Rotten Oranges / multi-source BFS
    13. Binary tree views using BFS
    14. Sliding Window Maximum using deque
    15. First negative in every window
    16. First non-repeating character in stream
    17. Generate binary numbers
    18. Josephus problem
    19. Task scheduling / CPU scheduling patterns
    20. Monotonic deque templates
    21. 0-1 BFS
    22. Topological sorting using Kahn's algorithm
    23. BFS grid templates
    24. Placement revision checklist

Python only.
"""

from collections import deque
import heapq


# ============================================================
# 0. QUEUE THEORY + COMPLEXITY
# ============================================================

"""
QUEUE = FIFO
First In, First Out

Core operations:
    enqueue(x) / append(x) -> add at rear
    dequeue() / popleft()  -> remove from front
    front()                -> inspect front
    rear()                 -> inspect rear
    is_empty()
    size()

Typical complexity:
    enqueue       O(1)
    dequeue       O(1)
    front         O(1)
    rear          O(1)

Important:
    Python list.pop(0) is O(n).
    Prefer collections.deque for a real queue.

Applications:
    - BFS
    - Level-order traversal
    - Scheduling
    - Producer-consumer systems
    - Buffers
    - OS scheduling
    - Networking
    - Multi-source BFS
    - Topological sorting
"""


# ============================================================
# 1. ARRAY / LIST BASED QUEUE
# ============================================================

class SimpleQueue:
    """
    Educational implementation.

    This uses a front pointer rather than pop(0), so dequeue is O(1)
    amortized/operationally, although unused prefix memory remains.
    """

    def __init__(self):
        self.items = []
        self.front_index = 0

    def enqueue(self, value):
        self.items.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        value = self.items[self.front_index]
        self.front_index += 1

        # Compact occasionally.
        if self.front_index > 100 and self.front_index * 2 > len(self.items):
            self.items = self.items[self.front_index:]
            self.front_index = 0

        return value

    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        return self.items[self.front_index]

    def rear(self):
        if self.is_empty():
            raise IndexError("Queue is empty")

        return self.items[-1]

    def is_empty(self):
        return self.front_index >= len(self.items)

    def size(self):
        return len(self.items) - self.front_index


# ============================================================
# 2. DEQUE BASED QUEUE
# ============================================================

class DequeQueue:
    """
    Production-friendly Python queue.

    collections.deque:
        append      O(1)
        popleft     O(1)
        appendleft  O(1)
        pop         O(1)
    """

    def __init__(self):
        self.q = deque()

    def enqueue(self, value):
        self.q.append(value)

    def dequeue(self):
        if not self.q:
            raise IndexError("Queue is empty")

        return self.q.popleft()

    def front(self):
        if not self.q:
            raise IndexError("Queue is empty")

        return self.q[0]

    def rear(self):
        if not self.q:
            raise IndexError("Queue is empty")

        return self.q[-1]

    def is_empty(self):
        return not self.q

    def size(self):
        return len(self.q)


# ============================================================
# 3. LINKED-LIST BASED QUEUE
# ============================================================

class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedQueue:
    """
    Keep both front and rear pointers.

    enqueue -> rear
    dequeue -> front

    Both O(1).
    """

    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def enqueue(self, value):
        node = QueueNode(value)

        if self.rear_node is None:
            self.front_node = self.rear_node = node
        else:
            self.rear_node.next = node
            self.rear_node = node

        self._size += 1

    def dequeue(self):
        if self.front_node is None:
            raise IndexError("Queue is empty")

        value = self.front_node.value
        self.front_node = self.front_node.next

        if self.front_node is None:
            self.rear_node = None

        self._size -= 1

        return value

    def front(self):
        if self.front_node is None:
            raise IndexError("Queue is empty")

        return self.front_node.value

    def rear(self):
        if self.rear_node is None:
            raise IndexError("Queue is empty")

        return self.rear_node.value

    def is_empty(self):
        return self.front_node is None

    def size(self):
        return self._size


# ============================================================
# 4. CIRCULAR QUEUE
# ============================================================

class CircularQueue:
    """
    Fixed-size circular queue.

    Important variables:
        front -> index of first element
        rear  -> next insertion position
        size  -> current number of elements

    All core operations O(1).
    """

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.data = [None] * capacity
        self.front_index = 0
        self.rear_index = 0
        self._size = 0

    def enqueue(self, value):
        if self.is_full():
            raise OverflowError("Circular queue is full")

        self.data[self.rear_index] = value
        self.rear_index = (self.rear_index + 1) % self.capacity
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Circular queue is empty")

        value = self.data[self.front_index]
        self.data[self.front_index] = None
        self.front_index = (self.front_index + 1) % self.capacity
        self._size -= 1

        return value

    def front(self):
        if self.is_empty():
            raise IndexError("Circular queue is empty")

        return self.data[self.front_index]

    def rear(self):
        if self.is_empty():
            raise IndexError("Circular queue is empty")

        index = (self.rear_index - 1) % self.capacity
        return self.data[index]

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self.capacity

    def size(self):
        return self._size


# ============================================================
# 5. DEQUE IMPLEMENTATION
# ============================================================

class MyDeque:
    """
    Educational deque using a doubly linked list.
    """

    class Node:
        def __init__(self, value):
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def append_left(self, value):
        node = self.Node(value)

        if not self.front_node:
            self.front_node = self.rear_node = node
        else:
            node.next = self.front_node
            self.front_node.prev = node
            self.front_node = node

        self._size += 1

    def append_right(self, value):
        node = self.Node(value)

        if not self.rear_node:
            self.front_node = self.rear_node = node
        else:
            node.prev = self.rear_node
            self.rear_node.next = node
            self.rear_node = node

        self._size += 1

    def pop_left(self):
        if not self.front_node:
            raise IndexError("Deque is empty")

        value = self.front_node.value
        self.front_node = self.front_node.next

        if self.front_node:
            self.front_node.prev = None
        else:
            self.rear_node = None

        self._size -= 1
        return value

    def pop_right(self):
        if not self.rear_node:
            raise IndexError("Deque is empty")

        value = self.rear_node.value
        self.rear_node = self.rear_node.prev

        if self.rear_node:
            self.rear_node.next = None
        else:
            self.front_node = None

        self._size -= 1
        return value

    def front(self):
        if not self.front_node:
            raise IndexError("Deque is empty")
        return self.front_node.value

    def rear(self):
        if not self.rear_node:
            raise IndexError("Deque is empty")
        return self.rear_node.value

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size


# ============================================================
# 6. PRIORITY QUEUE — MIN HEAP
# ============================================================

class MinPriorityQueue:
    """
    Python's heapq implements a min heap.

    push    O(log n)
    pop     O(log n)
    peek    O(1)
    """

    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, value)

    def pop(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")

        return heapq.heappop(self.heap)

    def peek(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")

        return self.heap[0]

    def is_empty(self):
        return not self.heap

    def size(self):
        return len(self.heap)


# ============================================================
# 7. PRIORITY QUEUE — MAX HEAP
# ============================================================

class MaxPriorityQueue:
    """
    Python's heapq is a min heap.

    Store negative values to simulate a max heap.
    """

    def __init__(self):
        self.heap = []

    def push(self, value):
        heapq.heappush(self.heap, -value)

    def pop(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")

        return -heapq.heappop(self.heap)

    def peek(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")

        return -self.heap[0]

    def is_empty(self):
        return not self.heap


# ============================================================
# 8. PRIORITY QUEUE WITH (PRIORITY, VALUE)
# ============================================================

class TaskPriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0

    def push(self, priority, task):
        """
        Smaller priority number = higher priority.
        counter gives stable ordering for equal priorities.
        """
        heapq.heappush(
            self.heap,
            (priority, self.counter, task)
        )
        self.counter += 1

    def pop(self):
        if not self.heap:
            raise IndexError("Priority queue is empty")

        _, _, task = heapq.heappop(self.heap)
        return task


# ============================================================
# 9. QUEUE USING TWO STACKS
# ============================================================

class QueueUsingTwoStacks:
    """
    Amortized O(1) queue.

    input_stack:
        receives new elements.

    output_stack:
        serves oldest elements.
    """

    def __init__(self):
        self.input_stack = []
        self.output_stack = []

    def _transfer(self):
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(
                    self.input_stack.pop()
                )

    def enqueue(self, value):
        self.input_stack.append(value)

    def dequeue(self):
        self._transfer()

        if not self.output_stack:
            raise IndexError("Queue is empty")

        return self.output_stack.pop()

    def peek(self):
        self._transfer()

        if not self.output_stack:
            raise IndexError("Queue is empty")

        return self.output_stack[-1]

    def empty(self):
        return not self.input_stack and not self.output_stack


# ============================================================
# 10. STACK USING TWO QUEUES
# ============================================================

class StackUsingTwoQueues:
    """
    Connection between Queue and Stack.

    Push O(n)
    Pop O(1)
    """

    def __init__(self):
        self.q = deque()

    def push(self, value):
        self.q.append(value)

        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        if not self.q:
            raise IndexError("Stack is empty")

        return self.q.popleft()

    def top(self):
        if not self.q:
            raise IndexError("Stack is empty")

        return self.q[0]

    def empty(self):
        return not self.q


# ============================================================
# 11. BFS — GRAPH
# ============================================================

def bfs_graph(graph, start):
    """
    graph:
        {
            node: [neighbors]
        }

    O(V + E)
    """
    visited = {start}
    q = deque([start])
    order = []

    while q:
        node = q.popleft()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)

    return order


# ============================================================
# 12. BFS — SHORTEST PATH IN UNWEIGHTED GRAPH
# ============================================================

def shortest_path_unweighted(graph, start, target):
    """
    BFS gives shortest number of edges in an unweighted graph.
    """

    q = deque([start])
    distance = {start: 0}

    while q:
        node = q.popleft()

        if node == target:
            return distance[node]

        for neighbor in graph.get(node, []):
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                q.append(neighbor)

    return -1


# ============================================================
# 13. BFS WITH PATH RECONSTRUCTION
# ============================================================

def shortest_path_with_path(graph, start, target):
    parent = {start: None}
    q = deque([start])

    while q:
        node = q.popleft()

        if node == target:
            break

        for neighbor in graph.get(node, []):
            if neighbor not in parent:
                parent[neighbor] = node
                q.append(neighbor)

    if target not in parent:
        return []

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


# ============================================================
# 14. BFS — CONNECTED COMPONENTS
# ============================================================

def count_components(graph, nodes):
    visited = set()
    count = 0

    for start in nodes:
        if start in visited:
            continue

        count += 1
        q = deque([start])
        visited.add(start)

        while q:
            node = q.popleft()

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)

    return count


# ============================================================
# 15. BINARY TREE NODE
# ============================================================

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# ============================================================
# 16. LEVEL ORDER TRAVERSAL
# ============================================================

def level_order(root):
    if root is None:
        return []

    result = []
    q = deque([root])

    while q:
        level = []

        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.value)

            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

        result.append(level)

    return result


# ============================================================
# 17. BINARY TREE RIGHT SIDE VIEW
# ============================================================

def right_side_view(root):
    if root is None:
        return []

    result = []
    q = deque([root])

    while q:
        level_size = len(q)

        for i in range(level_size):
            node = q.popleft()

            if i == level_size - 1:
                result.append(node.value)

            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

    return result


# ============================================================
# 18. BINARY TREE LEFT SIDE VIEW
# ============================================================

def left_side_view(root):
    if root is None:
        return []

    result = []
    q = deque([root])

    while q:
        level_size = len(q)

        for i in range(level_size):
            node = q.popleft()

            if i == 0:
                result.append(node.value)

            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

    return result


# ============================================================
# 19. AVERAGE OF LEVELS IN BINARY TREE
# ============================================================

def average_of_levels(root):
    if root is None:
        return []

    result = []
    q = deque([root])

    while q:
        total = 0
        count = len(q)

        for _ in range(count):
            node = q.popleft()
            total += node.value

            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

        result.append(total / count)

    return result


# ============================================================
# 20. MINIMUM DEPTH OF BINARY TREE
# ============================================================

def minimum_depth(root):
    if root is None:
        return 0

    q = deque([(root, 1)])

    while q:
        node, depth = q.popleft()

        if node.left is None and node.right is None:
            return depth

        if node.left:
            q.append((node.left, depth + 1))

        if node.right:
            q.append((node.right, depth + 1))

    return 0


# ============================================================
# 21. ROTTEN ORANGES — MULTI-SOURCE BFS
# ============================================================

def oranges_rotting(grid):
    """
    0 = empty
    1 = fresh
    2 = rotten

    All rotten oranges start simultaneously.
    Therefore use multi-source BFS.
    """

    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    q = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    minutes = 0

    while q:
        r, c, time = q.popleft()
        minutes = max(minutes, time)

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == 1
            ):
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, time + 1))

    return minutes if fresh == 0 else -1


# ============================================================
# 22. NUMBER OF ISLANDS — BFS
# ============================================================

def num_islands_bfs(grid):
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    islands = 0

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue

            islands += 1
            grid[r][c] = "0"

            q = deque([(r, c)])

            while q:
                cr, cc = q.popleft()

                for dr, dc in directions:
                    nr = cr + dr
                    nc = cc + dc

                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == "1"
                    ):
                        grid[nr][nc] = "0"
                        q.append((nr, nc))

    return islands


# ============================================================
# 23. FLOOD FILL — BFS
# ============================================================

def flood_fill(image, sr, sc, color):
    old_color = image[sr][sc]

    if old_color == color:
        return image

    rows = len(image)
    cols = len(image[0])

    q = deque([(sr, sc)])
    image[sr][sc] = color

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while q:
        r, c = q.popleft()

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and image[nr][nc] == old_color
            ):
                image[nr][nc] = color
                q.append((nr, nc))

    return image


# ============================================================
# 24. SLIDING WINDOW MAXIMUM — MONOTONIC DEQUE
# ============================================================

def max_sliding_window(nums, k):
    """
    Deque stores indices.

    Values are maintained in decreasing order.

    Front = maximum of current window.

    O(n).
    """

    if not nums or k == 0:
        return []

    q = deque()
    result = []

    for i, value in enumerate(nums):

        # Remove indices outside window.
        while q and q[0] <= i - k:
            q.popleft()

        # Remove smaller values from the back.
        while q and nums[q[-1]] <= value:
            q.pop()

        q.append(i)

        if i >= k - 1:
            result.append(nums[q[0]])

    return result


# ============================================================
# 25. SLIDING WINDOW MINIMUM — MONOTONIC DEQUE
# ============================================================

def min_sliding_window(nums, k):
    if not nums or k == 0:
        return []

    q = deque()
    result = []

    for i, value in enumerate(nums):

        while q and q[0] <= i - k:
            q.popleft()

        while q and nums[q[-1]] >= value:
            q.pop()

        q.append(i)

        if i >= k - 1:
            result.append(nums[q[0]])

    return result


# ============================================================
# 26. FIRST NEGATIVE NUMBER IN EVERY WINDOW
# ============================================================

def first_negative_in_window(nums, k):
    """
    Deque stores indices of negative numbers.
    """

    q = deque()
    result = []

    for i, value in enumerate(nums):

        if value < 0:
            q.append(i)

        while q and q[0] <= i - k:
            q.popleft()

        if i >= k - 1:
            result.append(
                nums[q[0]] if q else 0
            )

    return result


# ============================================================
# 27. FIRST NON-REPEATING CHARACTER IN STREAM
# ============================================================

def first_non_repeating_stream(stream):
    """
    For every prefix, return the first character whose
    frequency is currently 1.

    Queue holds candidates.
    """

    frequency = {}
    q = deque()
    result = []

    for ch in stream:
        frequency[ch] = frequency.get(ch, 0) + 1
        q.append(ch)

        while q and frequency[q[0]] > 1:
            q.popleft()

        result.append(q[0] if q else "#")

    return result


# ============================================================
# 28. GENERATE BINARY NUMBERS FROM 1 TO N
# ============================================================

def generate_binary_numbers(n):
    """
    Queue-based generation.

    Start with 1.
    For x:
        append x + "0"
        append x + "1"
    """

    if n <= 0:
        return []

    result = []
    q = deque(["1"])

    for _ in range(n):
        current = q.popleft()
        result.append(current)

        q.append(current + "0")
        q.append(current + "1")

    return result


# ============================================================
# 29. JOSEPHUS PROBLEM — QUEUE SIMULATION
# ============================================================

def josephus(n, k):
    """
    Returns the surviving position (1-indexed).

    Queue simulation:
        O(n*k) approximately.

    There is also an O(n) mathematical recurrence.
    """

    if n <= 0 or k <= 0:
        raise ValueError("n and k must be positive")

    q = deque(range(1, n + 1))

    while len(q) > 1:
        for _ in range(k - 1):
            q.append(q.popleft())

        q.popleft()

    return q[0]


def josephus_math(n, k):
    """
    O(n) recurrence.

    J(1, k) = 0
    J(n, k) = (J(n-1, k) + k) % n

    Returns 1-indexed answer.
    """

    survivor = 0

    for size in range(2, n + 1):
        survivor = (survivor + k) % size

    return survivor + 1


# ============================================================
# 30. CPU / TASK SCHEDULING — ROUND ROBIN SIMULATION
# ============================================================

def round_robin(tasks, quantum):
    """
    tasks:
        [(task_name, execution_time), ...]

    Returns completion order.

    Useful for understanding:
        FIFO
        cyclic processing
        OS scheduling
    """

    if quantum <= 0:
        raise ValueError("Quantum must be positive")

    q = deque(
        [list(task) for task in tasks]
    )

    completed = []

    while q:
        name, remaining = q.popleft()

        remaining -= quantum

        if remaining <= 0:
            completed.append(name)
        else:
            q.append([name, remaining])

    return completed


# ============================================================
# 31. KAHN'S ALGORITHM — TOPOLOGICAL SORT
# ============================================================

def topological_sort_kahn(num_nodes, edges):
    """
    edges:
        [(u, v), ...] means u -> v

    Uses:
        indegree + queue

    O(V + E)

    If result has fewer than V nodes:
        graph contains a cycle.
    """

    graph = [[] for _ in range(num_nodes)]
    indegree = [0] * num_nodes

    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    q = deque(
        i for i in range(num_nodes)
        if indegree[i] == 0
    )

    order = []

    while q:
        node = q.popleft()
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                q.append(neighbor)

    if len(order) != num_nodes:
        return []

    return order


# ============================================================
# 32. COURSE SCHEDULE — CAN FINISH?
# ============================================================

def can_finish_courses(num_courses, prerequisites):
    """
    prerequisites:
        [course, prerequisite]

    Equivalent to cycle detection in directed graph.
    """

    order = topological_sort_kahn(
        num_courses,
        [(pre, course) for course, pre in prerequisites]
    )

    return len(order) == num_courses


# ============================================================
# 33. 0-1 BFS
# ============================================================

def zero_one_bfs(graph, start):
    """
    graph:
        graph[u] = [(v, weight), ...]

    Weight must be 0 or 1.

    0-edge -> pushleft
    1-edge -> pushright

    O(V + E)
    """

    INF = float("inf")
    distance = {node: INF for node in graph}
    distance[start] = 0

    q = deque([start])

    while q:
        node = q.popleft()

        for neighbor, weight in graph.get(node, []):
            new_distance = distance[node] + weight

            if new_distance < distance.get(neighbor, INF):
                distance[neighbor] = new_distance

                if weight == 0:
                    q.appendleft(neighbor)
                else:
                    q.append(neighbor)

    return distance


# ============================================================
# 34. BFS GRID SHORTEST PATH
# ============================================================

def shortest_path_grid(grid, start, target):
    """
    Assumes:
        0 = open
        1 = blocked

    Returns minimum number of moves.
    """

    if not grid:
        return -1

    rows = len(grid)
    cols = len(grid[0])

    sr, sc = start
    tr, tc = target

    if (
        grid[sr][sc] == 1
        or grid[tr][tc] == 1
    ):
        return -1

    q = deque([(sr, sc, 0)])
    visited = {(sr, sc)}

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while q:
        r, c, distance = q.popleft()

        if (r, c) == (tr, tc):
            return distance

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] == 0
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                q.append((nr, nc, distance + 1))

    return -1


# ============================================================
# 35. MULTI-SOURCE BFS TEMPLATE
# ============================================================

def multi_source_bfs_template(sources, neighbors):
    """
    Generic pattern.

    sources:
        initial states at distance 0.

    neighbors(node):
        yields neighboring states.

    Useful for:
        - Rotten Oranges
        - Walls and Gates
        - Distance from nearest source
        - Fire spreading
        - Infection simulation
    """

    q = deque()
    distance = {}

    for source in sources:
        q.append(source)
        distance[source] = 0

    while q:
        node = q.popleft()

        for neighbor in neighbors(node):
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                q.append(neighbor)

    return distance


# ============================================================
# 36. LEVEL-BY-LEVEL BFS TEMPLATE
# ============================================================

def level_bfs_template(start):
    """
    Generic template when the problem asks:
        - minimum time
        - levels
        - number of rounds
        - distance in unweighted graph
    """

    q = deque([start])
    levels = 0

    while q:
        level_size = len(q)

        for _ in range(level_size):
            node = q.popleft()

            # Process node.

            # Add neighbors:
            # q.append(neighbor)

        levels += 1

    return levels


# ============================================================
# 37. SLIDING WINDOW DEQUE TEMPLATE
# ============================================================

def monotonic_deque_max_template(nums, k):
    """
    Generic maximum-window template.

    Deque stores indices.
    Values decrease from front to back.
    """

    q = deque()
    result = []

    for i, value in enumerate(nums):

        # 1. Remove expired indices.
        while q and q[0] <= i - k:
            q.popleft()

        # 2. Remove useless smaller elements.
        while q and nums[q[-1]] <= value:
            q.pop()

        # 3. Add current index.
        q.append(i)

        # 4. Window is valid.
        if i >= k - 1:
            result.append(nums[q[0]])

    return result


# ============================================================
# 38. QUEUE REVERSAL
# ============================================================

def reverse_queue(q):
    """
    Reverse a queue using a stack.
    """

    stack = []

    while q:
        stack.append(q.popleft())

    while stack:
        q.append(stack.pop())

    return q


# ============================================================
# 39. REVERSE FIRST K ELEMENTS OF QUEUE
# ============================================================

def reverse_first_k(q, k):
    if k < 0 or k > len(q):
        raise ValueError("Invalid k")

    stack = []

    for _ in range(k):
        stack.append(q.popleft())

    while stack:
        q.append(stack.pop())

    for _ in range(len(q) - k):
        q.append(q.popleft())

    return q


# ============================================================
# 40. INTERLEAVE FIRST HALF AND SECOND HALF
# ============================================================

def interleave_queue(q):
    """
    Example:
        [1,2,3,4]
        -> [1,3,2,4]

    Assumes even length.
    """

    if len(q) % 2 != 0:
        raise ValueError("Queue size must be even")

    half = len(q) // 2
    first_half = deque()

    for _ in range(half):
        first_half.append(q.popleft())

    while first_half:
        q.append(first_half.popleft())
        q.append(q.popleft())

    return q


# ============================================================
# 41. CHECK QUEUE SORTED
# ============================================================

def is_queue_sorted(q):
    """
    Checks non-decreasing order without destroying the queue.
    """

    if len(q) <= 1:
        return True

    values = list(q)

    return all(
        values[i] <= values[i + 1]
        for i in range(len(values) - 1)
    )


# ============================================================
# 42. PRIORITY QUEUE — KTH LARGEST
# ============================================================

def kth_largest(nums, k):
    """
    Min heap of size k.

    O(n log k)
    """

    if k <= 0 or k > len(nums):
        raise ValueError("Invalid k")

    heap = []

    for value in nums:
        heapq.heappush(heap, value)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


# ============================================================
# 43. MERGE K SORTED ARRAYS
# ============================================================

def merge_k_sorted_arrays(arrays):
    """
    Min heap stores:
        (value, array_index, element_index)

    Complexity:
        O(N log k)
    """

    heap = []
    result = []

    for array_index, array in enumerate(arrays):
        if array:
            heapq.heappush(
                heap,
                (array[0], array_index, 0)
            )

    while heap:
        value, array_index, element_index = heapq.heappop(heap)
        result.append(value)

        next_index = element_index + 1

        if next_index < len(arrays[array_index]):
            heapq.heappush(
                heap,
                (
                    arrays[array_index][next_index],
                    array_index,
                    next_index
                )
            )

    return result


# ============================================================
# 44. K CLOSEST POINTS — PRIORITY QUEUE
# ============================================================

def k_closest_points(points, k):
    """
    Uses a max heap of size k.

    Distance squared:
        x*x + y*y
    """

    heap = []

    for x, y in points:
        distance = x * x + y * y

        heapq.heappush(
            heap,
            (-distance, x, y)
        )

        if len(heap) > k:
            heapq.heappop(heap)

    return [(x, y) for _, x, y in heap]


# ============================================================
# 45. TASK SCHEDULER — PRIORITY QUEUE + COOLDOWN
# ============================================================

def task_scheduler(tasks, cooldown):
    """
    Conceptual simulation.

    tasks:
        list of task labels.

    Uses:
        max heap + cooldown queue.

    Returns minimum time units.
    """

    from collections import Counter

    frequency = Counter(tasks)
    heap = [-count for count in frequency.values()]
    heapq.heapify(heap)

    cooldown_queue = deque()
    time = 0

    while heap or cooldown_queue:
        time += 1

        if heap:
            remaining = heapq.heappop(heap) + 1

            if remaining != 0:
                cooldown_queue.append(
                    (time + cooldown, remaining)
                )

        if cooldown_queue and cooldown_queue[0][0] == time:
            _, remaining = cooldown_queue.popleft()
            heapq.heappush(heap, remaining)

    return time


# ============================================================
# 46. BFS WORD LADDER
# ============================================================

def word_ladder_length(begin_word, end_word, word_list):
    """
    BFS over implicit graph.

    Each word differs by one character from neighbors.
    """

    words = set(word_list)

    if end_word not in words:
        return 0

    q = deque([(begin_word, 1)])
    visited = {begin_word}

    while q:
        word, distance = q.popleft()

        if word == end_word:
            return distance

        chars = list(word)

        for i in range(len(chars)):
            original = chars[i]

            for code in range(ord("a"), ord("z") + 1):
                chars[i] = chr(code)
                candidate = "".join(chars)

                if (
                    candidate in words
                    and candidate not in visited
                ):
                    visited.add(candidate)
                    q.append(
                        (candidate, distance + 1)
                    )

            chars[i] = original

    return 0


# ============================================================
# 47. TEST HELPERS
# ============================================================

def run_revision_tests():

    # Simple Queue
    q = SimpleQueue()
    q.enqueue(10)
    q.enqueue(20)

    assert q.front() == 10
    assert q.rear() == 20
    assert q.dequeue() == 10
    assert q.size() == 1

    # Deque queue
    dq = DequeQueue()
    dq.enqueue(1)
    dq.enqueue(2)

    assert dq.dequeue() == 1
    assert dq.front() == 2

    # Linked Queue
    lq = LinkedQueue()
    lq.enqueue(5)
    lq.enqueue(6)

    assert lq.front() == 5
    assert lq.rear() == 6
    assert lq.dequeue() == 5

    # Circular Queue
    cq = CircularQueue(3)

    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)

    assert cq.is_full()
    assert cq.dequeue() == 1

    cq.enqueue(4)

    assert cq.rear() == 4

    # Deque
    custom_deque = MyDeque()
    custom_deque.append_right(2)
    custom_deque.append_left(1)
    custom_deque.append_right(3)

    assert custom_deque.front() == 1
    assert custom_deque.rear() == 3
    assert custom_deque.pop_left() == 1
    assert custom_deque.pop_right() == 3

    # Priority Queue
    pq = MinPriorityQueue()

    pq.push(5)
    pq.push(1)
    pq.push(3)

    assert pq.pop() == 1
    assert pq.peek() == 3

    # Queue using stacks
    qs = QueueUsingTwoStacks()

    qs.enqueue(1)
    qs.enqueue(2)

    assert qs.peek() == 1
    assert qs.dequeue() == 1

    # Stack using queues
    sq = StackUsingTwoQueues()

    sq.push(1)
    sq.push(2)

    assert sq.top() == 2
    assert sq.pop() == 2

    # Graph BFS
    graph = {
        1: [2, 3],
        2: [4],
        3: [],
        4: []
    }

    assert bfs_graph(graph, 1) == [1, 2, 3, 4]

    assert shortest_path_unweighted(
        graph, 1, 4
    ) == 2

    assert shortest_path_with_path(
        graph, 1, 4
    ) == [1, 2, 4]

    # Tree BFS
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    assert level_order(root) == [
        [1],
        [2, 3],
        [4, 5]
    ]

    assert right_side_view(root) == [1, 3, 5]
    assert left_side_view(root) == [1, 2, 4]

    # Sliding window maximum
    assert max_sliding_window(
        [1, 3, -1, -3, 5, 3, 6, 7],
        3
    ) == [3, 3, 5, 5, 6, 7]

    # Sliding window minimum
    assert min_sliding_window(
        [1, 3, -1, -3, 5, 3, 6, 7],
        3
    ) == [ -1, -3, -3, -3, 3, 3]

    # First negative
    assert first_negative_in_window(
        [12, -1, -7, 8, -15, 30, 16, 28],
        3
    ) == [-1, -1, -7, -15, -15, 0]

    # First non-repeating stream
    assert first_non_repeating_stream(
        "aabc"
    ) == ["a", "#", "b", "b"]

    # Binary numbers
    assert generate_binary_numbers(5) == [
        "1", "10", "11", "100", "101"
    ]

    # Josephus
    assert josephus_math(5, 2) == 3

    # Topological sort
    order = topological_sort_kahn(
        4,
        [(0, 1), (0, 2), (1, 3), (2, 3)]
    )

    assert order

    # Course schedule
    assert can_finish_courses(
        2,
        [[1, 0]]
    )

    assert not can_finish_courses(
        2,
        [[1, 0], [0, 1]]
    )

    # Kth largest
    assert kth_largest(
        [3, 2, 1, 5, 6, 4], 2
    ) == 5

    # Merge K sorted arrays
    assert merge_k_sorted_arrays(
        [[1, 4, 7], [2, 5], [3, 6]]
    ) == [1, 2, 3, 4, 5, 6, 7]

    print("All Queue revision tests passed! ✓")


# ============================================================
# 48. PLACEMENT REVISION CHECKLIST
# ============================================================

"""
QUEUE FUNDAMENTALS
[ ] Understand FIFO
[ ] enqueue
[ ] dequeue
[ ] front
[ ] rear
[ ] is_empty
[ ] size
[ ] Overflow / underflow
[ ] Why list.pop(0) is O(n)
[ ] Why deque.popleft() is O(1)

IMPLEMENTATIONS
[ ] Array/list queue
[ ] Queue with front pointer
[ ] Linked-list queue
[ ] Circular queue
[ ] Deque
[ ] Priority Queue
[ ] Min Heap
[ ] Max Heap

DESIGN QUESTIONS
[ ] Queue using two stacks
[ ] Stack using two queues
[ ] Why queue using two stacks is amortized O(1)
[ ] Circular queue and modulo arithmetic
[ ] Why maintain front + rear pointers?
[ ] Array queue vs linked-list queue
[ ] Queue vs deque
[ ] Queue vs priority queue

BFS
[ ] Basic graph BFS
[ ] BFS traversal
[ ] Connected components
[ ] Shortest path in unweighted graph
[ ] Path reconstruction
[ ] Grid BFS
[ ] Number of islands
[ ] Flood fill
[ ] Rotten oranges
[ ] Multi-source BFS
[ ] Word Ladder
[ ] Level-order tree traversal
[ ] Left view
[ ] Right view
[ ] Minimum depth

MONOTONIC DEQUE
[ ] Sliding Window Maximum
[ ] Sliding Window Minimum
[ ] First Negative in Window
[ ] Understand index-based deque
[ ] Remove expired indices
[ ] Remove dominated elements
[ ] Understand why each index enters/leaves once

PRIORITY QUEUE / HEAP
[ ] Min heap
[ ] Max heap
[ ] Kth largest
[ ] Merge K sorted arrays
[ ] K closest points
[ ] Task scheduling
[ ] Understand heap push/pop O(log n)
[ ] Understand heap peek O(1)

ADVANCED
[ ] Josephus
[ ] 0-1 BFS
[ ] Kahn's algorithm
[ ] Course Schedule
[ ] Round Robin scheduling
[ ] Queue reversal
[ ] Reverse first K elements
[ ] Interleave queue

MOST IMPORTANT PATTERN RECOGNITION

1. "First come, first served"
       -> Queue

2. "Shortest path in an unweighted graph"
       -> BFS / Queue

3. "Minimum number of rounds/time steps"
       -> BFS levels

4. "Multiple starting points spread simultaneously"
       -> Multi-source BFS

5. "Tree level by level"
       -> Queue

6. "Maximum/minimum in every sliding window"
       -> Monotonic Deque

7. "Need highest/lowest priority item"
       -> Priority Queue / Heap

8. "Dependencies / prerequisites"
       -> Topological Sort + Queue

9. "0/1 edge weights"
       -> 0-1 BFS + Deque

10. "Implement queue using stack"
       -> Two-stack amortized technique

11. "Implement stack using queue"
       -> Queue rotation

PLACEMENT STANDARD:

Do not memorize:
    "Rotten Oranges solution"
    "Sliding Window Maximum solution"
    "Course Schedule solution"

Instead recognize:
    Problem -> State -> Data Structure -> Invariant

Examples:

Rotten Oranges
    -> simultaneous spreading
    -> multi-source BFS
    -> queue stores current frontier

Sliding Window Maximum
    -> need maximum of moving window
    -> monotonic deque
    -> deque front is maximum

Course Schedule
    -> dependency graph
    -> indegree + queue
    -> process zero-indegree nodes

Kth Largest
    -> maintain only k useful candidates
    -> min heap of size k
    -> heap root is kth largest

Shortest path
    -> unweighted graph
    -> BFS
    -> first visit gives shortest distance
"""


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("QUEUE — COMPLETE REVISION LIBRARY")
    print("=" * 70)
    print()
    print("Basic Queue              ✓")
    print("Linked-List Queue        ✓")
    print("Circular Queue           ✓")
    print("Deque                    ✓")
    print("Priority Queue / Heap    ✓")
    print("Queue using Stacks       ✓")
    print("Stack using Queues       ✓")
    print("Graph BFS                ✓")
    print("Tree BFS                 ✓")
    print("Grid BFS                 ✓")
    print("Multi-source BFS         ✓")
    print("Monotonic Deque          ✓")
    print("Topological Sort         ✓")
    print("0-1 BFS                  ✓")
    print("Advanced Problems        ✓")
    print()
    print("Run run_revision_tests() to verify implementations.")
    print("=" * 70)

    # Uncomment:
    # run_revision_tests()

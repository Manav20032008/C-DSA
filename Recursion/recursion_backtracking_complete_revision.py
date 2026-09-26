"""
RECURSION + BACKTRACKING — COMPLETE REVISION
=============================================

Placement revision library:
- Recursion fundamentals
- Recursive arrays/strings
- Binary search
- Merge sort / Quick sort
- Linked-list recursion
- Tree recursion
- Memoization / recursive DP
- Subsets / permutations / combinations
- Combination Sum
- Parentheses
- Palindrome partitioning
- N-Queens
- Sudoku
- Word Search
- Rat in a Maze
- Graph Coloring
- Partitioning
- Generic recursion/backtracking templates
"""

from functools import lru_cache


# ============================================================
# RECURSION FUNDAMENTALS
# ============================================================

def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def power(x, n):
    if n < 0:
        return 1 / power(x, -n)
    if n == 0:
        return 1
    return x * power(x, n - 1)


def fast_power(x, n):
    """O(log n) exponentiation by divide and conquer."""
    if n < 0:
        return 1 / fast_power(x, -n)
    if n == 0:
        return 1

    half = fast_power(x, n // 2)

    if n % 2 == 0:
        return half * half

    return x * half * half


def fibonacci(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_memo(n):
    @lru_cache(maxsize=None)
    def solve(x):
        if x <= 1:
            return x
        return solve(x - 1) + solve(x - 2)

    return solve(n)


def sum_n(n):
    if n <= 0:
        return 0
    return n + sum_n(n - 1)


def digit_sum(n):
    n = abs(n)
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


def count_digits(n):
    n = abs(n)
    if n < 10:
        return 1
    return 1 + count_digits(n // 10)


def gcd(a, b):
    if b == 0:
        return abs(a)
    return gcd(b, a % b)


def reverse_string(s):
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


def is_palindrome(s, left=0, right=None):
    if right is None:
        right = len(s) - 1

    if left >= right:
        return True

    if s[left] != s[right]:
        return False

    return is_palindrome(s, left + 1, right - 1)


# ============================================================
# RECURSIVE ARRAY / SEARCH PROBLEMS
# ============================================================

def recursive_array_sum(nums, index=0):
    if index == len(nums):
        return 0
    return nums[index] + recursive_array_sum(nums, index + 1)


def recursive_max(nums, index=0):
    if not nums:
        raise ValueError("array cannot be empty")

    if index == len(nums) - 1:
        return nums[index]

    return max(nums[index], recursive_max(nums, index + 1))


def is_sorted_recursive(nums, index=0):
    if len(nums) <= 1 or index == len(nums) - 1:
        return True

    if nums[index] > nums[index + 1]:
        return False

    return is_sorted_recursive(nums, index + 1)


def first_occurrence(nums, target, index=0):
    if index == len(nums):
        return -1

    if nums[index] == target:
        return index

    return first_occurrence(nums, target, index + 1)


def last_occurrence(nums, target, index=0):
    if index == len(nums):
        return -1

    answer = last_occurrence(nums, target, index + 1)

    if answer != -1:
        return answer

    return index if nums[index] == target else -1


def binary_search_recursive(nums, target, left=0, right=None):
    if right is None:
        right = len(nums) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid

    if nums[mid] < target:
        return binary_search_recursive(nums, target, mid + 1, right)

    return binary_search_recursive(nums, target, left, mid - 1)


# ============================================================
# DIVIDE AND CONQUER
# ============================================================

def merge_sort(nums):
    if len(nums) <= 1:
        return nums[:]

    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(nums):
    if len(nums) <= 1:
        return nums[:]

    pivot = nums[-1]
    left = [x for x in nums[:-1] if x <= pivot]
    right = [x for x in nums[:-1] if x > pivot]

    return quick_sort(left) + [pivot] + quick_sort(right)


# ============================================================
# LINKED LIST RECURSION
# ============================================================

class ListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


def linked_list_to_list(head):
    if head is None:
        return []
    return [head.value] + linked_list_to_list(head.next)


def reverse_linked_list_recursive(head):
    if head is None or head.next is None:
        return head

    new_head = reverse_linked_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# ============================================================
# TREE RECURSION
# ============================================================

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def preorder(root):
    if root is None:
        return []
    return [root.value] + preorder(root.left) + preorder(root.right)


def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.value] + inorder(root.right)


def postorder(root):
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.value]


def tree_height(root):
    if root is None:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))


def tree_diameter(root):
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
# RECURSION + DP / MEMOIZATION
# ============================================================

def climbing_stairs(n):
    @lru_cache(maxsize=None)
    def solve(step):
        if step <= 1:
            return 1
        return solve(step - 1) + solve(step - 2)

    return solve(n)


def house_robber_recursive(nums):
    @lru_cache(maxsize=None)
    def solve(i):
        if i >= len(nums):
            return 0

        skip = solve(i + 1)
        take = nums[i] + solve(i + 2)
        return max(skip, take)

    return solve(0)


def target_sum_ways(nums, target):
    @lru_cache(maxsize=None)
    def solve(i, total):
        if i == len(nums):
            return int(total == target)

        return (
            solve(i + 1, total + nums[i])
            + solve(i + 1, total - nums[i])
        )

    return solve(0, 0)


def knapsack_01(weights, values, capacity):
    @lru_cache(maxsize=None)
    def solve(i, remaining):
        if i == len(weights):
            return 0

        best = solve(i + 1, remaining)

        if weights[i] <= remaining:
            best = max(
                best,
                values[i] + solve(i + 1, remaining - weights[i])
            )

        return best

    return solve(0, capacity)


# ============================================================
# BACKTRACKING — SUBSETS
# ============================================================

def subsets(nums):
    result = []
    path = []

    def backtrack(i):
        if i == len(nums):
            result.append(path[:])
            return

        # Do not choose.
        backtrack(i + 1)

        # Choose.
        path.append(nums[i])
        backtrack(i + 1)
        path.pop()

    backtrack(0)
    return result


def subsets_with_duplicates(nums):
    nums.sort()
    result = []

    def backtrack(start, path):
        result.append(path[:])

        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue

            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


# ============================================================
# BACKTRACKING — PERMUTATIONS
# ============================================================

def permutations(nums):
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            used[i] = True
            path.append(nums[i])

            backtrack()

            path.pop()
            used[i] = False

    backtrack()
    return result


def permutations_swap(nums):
    nums = nums[:]
    result = []

    def backtrack(i):
        if i == len(nums):
            result.append(nums[:])
            return

        for j in range(i, len(nums)):
            nums[i], nums[j] = nums[j], nums[i]
            backtrack(i + 1)
            nums[i], nums[j] = nums[j], nums[i]

    backtrack(0)
    return result


def permutations_with_duplicates(nums):
    nums.sort()
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue

            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return result


# ============================================================
# BACKTRACKING — COMBINATIONS
# ============================================================

def combinations(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return

        for x in range(start, n + 1):
            path.append(x)
            backtrack(x + 1, path)
            path.pop()

    backtrack(1, [])
    return result


def combination_sum(candidates, target):
    candidates = sorted(set(candidates))
    result = []

    def backtrack(start, remaining, path):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break

            path.append(candidates[i])
            backtrack(i, remaining - candidates[i], path)
            path.pop()

    backtrack(0, target, [])
    return result


def combination_sum_ii(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, remaining, path):
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            if candidates[i] > remaining:
                break

            path.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i], path)
            path.pop()

    backtrack(0, target, [])
    return result


def combination_sum_iii(k, target):
    result = []

    def backtrack(start, remaining, path):
        if len(path) == k:
            if remaining == 0:
                result.append(path[:])
            return

        for x in range(start, 10):
            if x > remaining:
                break

            path.append(x)
            backtrack(x + 1, remaining - x, path)
            path.pop()

    backtrack(1, target, [])
    return result


# ============================================================
# STRING BACKTRACKING
# ============================================================

def letter_combinations(digits):
    if not digits:
        return []

    mapping = {
        "2": "abc", "3": "def",
        "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs",
        "8": "tuv", "9": "wxyz"
    }

    result = []
    path = []

    def backtrack(i):
        if i == len(digits):
            result.append("".join(path))
            return

        for ch in mapping[digits[i]]:
            path.append(ch)
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


def generate_parentheses(n):
    result = []

    def backtrack(open_count, close_count, path):
        if len(path) == 2 * n:
            result.append("".join(path))
            return

        if open_count < n:
            path.append("(")
            backtrack(open_count + 1, close_count, path)
            path.pop()

        if close_count < open_count:
            path.append(")")
            backtrack(open_count, close_count + 1, path)
            path.pop()

    backtrack(0, 0, [])
    return result


def palindrome_partition(s):
    result = []
    path = []

    def is_pal(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    def backtrack(start):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            if not is_pal(start, end):
                continue

            path.append(s[start:end + 1])
            backtrack(end + 1)
            path.pop()

    backtrack(0)
    return result


def letter_case_permutation(s):
    result = []
    path = []

    def backtrack(i):
        if i == len(s):
            result.append("".join(path))
            return

        ch = s[i]

        if ch.isalpha():
            path.append(ch.lower())
            backtrack(i + 1)
            path.pop()

            path.append(ch.upper())
            backtrack(i + 1)
            path.pop()
        else:
            path.append(ch)
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


def restore_ip_addresses(s):
    result = []

    def backtrack(i, parts):
        if len(parts) == 4:
            if i == len(s):
                result.append(".".join(parts))
            return

        remaining = len(s) - i
        slots = 4 - len(parts)

        if remaining < slots or remaining > 3 * slots:
            return

        for length in range(1, 4):
            if i + length > len(s):
                break

            part = s[i:i + length]

            if len(part) > 1 and part[0] == "0":
                break

            if int(part) > 255:
                continue

            parts.append(part)
            backtrack(i + length, parts)
            parts.pop()

    backtrack(0, [])
    return result


# ============================================================
# GRID BACKTRACKING
# ============================================================

def word_search(board, word):
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def dfs(r, c, i):
        if i == len(word):
            return True

        if not (0 <= r < rows and 0 <= c < cols):
            return False

        if board[r][c] != word[i]:
            return False

        original = board[r][c]
        board[r][c] = "#"

        found = (
            dfs(r + 1, c, i + 1)
            or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1)
            or dfs(r, c - 1, i + 1)
        )

        board[r][c] = original
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False


def rat_in_maze(maze):
    n = len(maze)
    if not n or maze[0][0] == 0:
        return []

    result = []
    visited = [[False] * n for _ in range(n)]

    directions = [
        (1, 0, "D"),
        (0, -1, "L"),
        (0, 1, "R"),
        (-1, 0, "U")
    ]

    def backtrack(r, c, path):
        if r == n - 1 and c == n - 1:
            result.append("".join(path))
            return

        visited[r][c] = True

        for dr, dc, move in directions:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < n and
                0 <= nc < n and
                maze[nr][nc] == 1 and
                not visited[nr][nc]
            ):
                path.append(move)
                backtrack(nr, nc, path)
                path.pop()

        visited[r][c] = False

    backtrack(0, 0, [])
    return result


# ============================================================
# N-QUEENS
# ============================================================

def solve_n_queens(n):
    result = []
    board = [["."] * n for _ in range(n)]

    columns = set()
    diagonals = set()       # row - col
    anti_diagonals = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append(["".join(r) for r in board])
            return

        for col in range(n):
            d = row - col
            ad = row + col

            if col in columns or d in diagonals or ad in anti_diagonals:
                continue

            board[row][col] = "Q"
            columns.add(col)
            diagonals.add(d)
            anti_diagonals.add(ad)

            backtrack(row + 1)

            board[row][col] = "."
            columns.remove(col)
            diagonals.remove(d)
            anti_diagonals.remove(ad)

    backtrack(0)
    return result


def count_n_queens(n):
    columns = set()
    diagonals = set()
    anti_diagonals = set()

    def backtrack(row):
        if row == n:
            return 1

        count = 0

        for col in range(n):
            d = row - col
            ad = row + col

            if col in columns or d in diagonals or ad in anti_diagonals:
                continue

            columns.add(col)
            diagonals.add(d)
            anti_diagonals.add(ad)

            count += backtrack(row + 1)

            columns.remove(col)
            diagonals.remove(d)
            anti_diagonals.remove(ad)

        return count

    return backtrack(0)


# ============================================================
# SUDOKU
# ============================================================

def solve_sudoku(board):
    """Mutates a 9x9 board in-place. Empty cells are '.'."""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []

    for r in range(9):
        for c in range(9):
            value = board[r][c]

            if value == ".":
                empty.append((r, c))
            else:
                b = (r // 3) * 3 + c // 3
                rows[r].add(value)
                cols[c].add(value)
                boxes[b].add(value)

    def backtrack(index):
        if index == len(empty):
            return True

        r, c = empty[index]
        b = (r // 3) * 3 + c // 3

        for digit in "123456789":
            if digit in rows[r] or digit in cols[c] or digit in boxes[b]:
                continue

            board[r][c] = digit
            rows[r].add(digit)
            cols[c].add(digit)
            boxes[b].add(digit)

            if backtrack(index + 1):
                return True

            board[r][c] = "."
            rows[r].remove(digit)
            cols[c].remove(digit)
            boxes[b].remove(digit)

        return False

    return backtrack(0)


# ============================================================
# GRAPH COLORING
# ============================================================

def graph_coloring(graph, m):
    """graph is an adjacency matrix; returns colors or None."""
    n = len(graph)
    colors = [0] * n

    def valid(node, color):
        return all(
            not graph[node][neighbor] or colors[neighbor] != color
            for neighbor in range(n)
        )

    def backtrack(node):
        if node == n:
            return True

        for color in range(1, m + 1):
            if valid(node, color):
                colors[node] = color

                if backtrack(node + 1):
                    return True

                colors[node] = 0

        return False

    return colors if backtrack(0) else None


# ============================================================
# PARTITION / CONSTRAINT BACKTRACKING
# ============================================================

def can_partition_k_subsets(nums, k):
    total = sum(nums)

    if k <= 0 or total % k != 0:
        return False

    target = total // k
    nums = sorted(nums, reverse=True)
    buckets = [0] * k

    def backtrack(i):
        if i == len(nums):
            return True

        value = nums[i]

        for bucket in range(k):
            if buckets[bucket] + value > target:
                continue

            # Symmetry pruning.
            if bucket > 0 and buckets[bucket] == buckets[bucket - 1]:
                continue

            buckets[bucket] += value

            if backtrack(i + 1):
                return True

            buckets[bucket] -= value

        return False

    return backtrack(0)


# ============================================================
# BINARY STRING GENERATION
# ============================================================

def binary_strings(n):
    result = []

    def backtrack(path):
        if len(path) == n:
            result.append("".join(path))
            return

        for bit in ("0", "1"):
            path.append(bit)
            backtrack(path)
            path.pop()

    backtrack([])
    return result


def binary_strings_no_consecutive_ones(n):
    result = []

    def backtrack(path, previous):
        if len(path) == n:
            result.append("".join(path))
            return

        path.append("0")
        backtrack(path, 0)
        path.pop()

        if previous == 0:
            path.append("1")
            backtrack(path, 1)
            path.pop()

    backtrack([], 0)
    return result


# ============================================================
# RECURSIVE SUBSET / TARGET PROBLEMS
# ============================================================

def count_subsets_with_sum(nums, target):
    def solve(i, remaining):
        if i == len(nums):
            return int(remaining == 0)

        return (
            solve(i + 1, remaining)
            + (
                solve(i + 1, remaining - nums[i])
                if nums[i] <= remaining else 0
            )
        )

    return solve(0, target)


def target_sum_ways_naive(nums, target):
    def solve(i, total):
        if i == len(nums):
            return int(total == target)

        return (
            solve(i + 1, total + nums[i])
            + solve(i + 1, total - nums[i])
        )

    return solve(0, 0)


# ============================================================
# GENERIC TEMPLATES
# ============================================================

def recursion_template():
    """
    def solve(state):
        if base_case:
            return answer

        smaller_state = make_smaller(state)
        result = solve(smaller_state)

        return combine(state, result)

    Always identify:
        1. Base case
        2. Smaller subproblem
        3. Recursive relation
        4. Return/combine step
    """
    raise NotImplementedError


def backtracking_template():
    """
    def backtrack(state):
        if complete:
            record_answer()
            return

        for choice in choices:
            if invalid(choice):
                continue

            choose(choice)
            backtrack(new_state)
            undo(choice)

    Core idea:
        CHOOSE -> EXPLORE -> UNDO
    """
    raise NotImplementedError


def pruning_template():
    """
    Backtracking with pruning:

        if current_state_can_never_become_solution:
            return

    Useful pruning techniques:
        - sorted candidates
        - duplicate skipping
        - remaining-sum checks
        - constraint sets
        - symmetry breaking
        - early termination
    """
    raise NotImplementedError


# ============================================================
# PATTERN CHEAT SHEET
# ============================================================

"""
RECURSION
---------

Factorial:
    f(n) = n * f(n-1)

Binary Search:
    eliminate half -> O(log n)

Merge Sort:
    split + solve halves + merge -> O(n log n)

Fibonacci:
    overlapping subproblems -> memoization / DP

Tree:
    solve left + solve right + combine


BACKTRACKING
------------

SUBSETS:
    choose / don't choose
    O(2^n)

PERMUTATIONS:
    choose an unused element
    O(n!)

COMBINATIONS:
    maintain start index
    recurse with i+1

REUSABLE CANDIDATES:
    recurse with i

NO REUSE:
    recurse with i+1

DUPLICATES:
    sort first
    skip:
        if i > start and nums[i] == nums[i-1]

GRID:
    mark -> explore -> unmark

CONSTRAINT:
    choose -> validate -> recurse -> undo

N-QUEENS:
    columns
    row-col diagonals
    row+col diagonals

SUDOKU:
    row set
    column set
    3x3 box set


THE 7 QUESTIONS TO ASK IN AN INTERVIEW
---------------------------------------

1. What is my state?
2. What is my base case?
3. What are my choices?
4. What choices are invalid?
5. What state changes after choosing?
6. What must I undo?
7. Can I prune or memoize?


RECURSION VS BACKTRACKING
-------------------------

Recursion:
    "Solve a smaller version of this problem."

Backtracking:
    "Try one decision, explore it, undo it,
     then try another decision."

MEMOIZATION:
    Use when different recursive paths reach
    the same state.

BACKTRACKING:
    Use when you need to explore a decision tree
    and construct candidate solutions.


COMPLEXITY
----------

Factorial                 O(n)
Binary Search             O(log n)
Merge Sort                O(n log n)
Naive Fibonacci           O(2^n)
Subsets                   O(2^n) outputs
Permutations              O(n!)
N-Queens                  exponential
Sudoku                    exponential worst case

Remember:
    Output itself can impose a lower bound.

If there are 2^n subsets, merely outputting them
already requires Ω(2^n) work.


PLACEMENT CHECKLIST
-------------------

RECURSION
[ ] Base case
[ ] Recursive case
[ ] Stack frames
[ ] Recursion tree
[ ] Recurrence
[ ] Time complexity
[ ] Space complexity
[ ] Stack overflow
[ ] Factorial
[ ] Fibonacci
[ ] Power
[ ] Fast power
[ ] Digit sum
[ ] GCD
[ ] Palindrome
[ ] Binary search

DIVIDE & CONQUER
[ ] Merge sort
[ ] Quick sort
[ ] Fast exponentiation

RECURSIVE DATA STRUCTURES
[ ] Linked list traversal
[ ] Reverse linked list
[ ] Tree traversals
[ ] Tree height
[ ] Tree diameter

RECURSION + DP
[ ] Memoization
[ ] Climbing stairs
[ ] House robber
[ ] Target sum
[ ] Knapsack

BACKTRACKING
[ ] Decision tree
[ ] State
[ ] Choice
[ ] Constraint
[ ] Choose
[ ] Explore
[ ] Undo
[ ] Pruning

SUBSETS / COMBINATIONS
[ ] Subsets
[ ] Subsets II
[ ] Combinations
[ ] Combination Sum
[ ] Combination Sum II
[ ] Combination Sum III

PERMUTATIONS
[ ] Used-array method
[ ] Swap method
[ ] Duplicate permutations

STRINGS
[ ] Phone combinations
[ ] Generate parentheses
[ ] Palindrome partitioning
[ ] Letter case permutation
[ ] Restore IP addresses

GRID / CONSTRAINT
[ ] Word Search
[ ] Rat in Maze
[ ] N-Queens
[ ] Sudoku
[ ] Graph Coloring
[ ] K equal subsets
"""


# ============================================================
# TEST SUITE
# ============================================================

def run_revision_tests():
    assert factorial(5) == 120
    assert fast_power(2, 10) == 1024
    assert fibonacci(10) == 55
    assert fibonacci_memo(30) == 832040
    assert sum_n(5) == 15
    assert digit_sum(12345) == 15
    assert count_digits(12345) == 5
    assert gcd(48, 18) == 6
    assert reverse_string("hello") == "olleh"
    assert is_palindrome("racecar")

    nums = [1, 2, 2, 5]
    assert recursive_array_sum(nums) == 10
    assert recursive_max(nums) == 5
    assert is_sorted_recursive(nums)
    assert first_occurrence(nums, 2) == 1
    assert last_occurrence(nums, 2) == 2
    assert binary_search_recursive(nums, 5) == 3

    assert merge_sort([5, 1, 4, 2, 3]) == [1, 2, 3, 4, 5]
    assert quick_sort([5, 1, 4, 2, 3]) == [1, 2, 3, 4, 5]

    head = ListNode(1, ListNode(2, ListNode(3)))
    head = reverse_linked_list_recursive(head)
    assert linked_list_to_list(head) == [3, 2, 1]

    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    assert preorder(root) == [1, 2, 4, 5, 3]
    assert inorder(root) == [4, 2, 5, 1, 3]
    assert postorder(root) == [4, 5, 2, 3, 1]
    assert tree_height(root) == 3
    assert tree_diameter(root) == 3

    assert climbing_stairs(5) == 8
    assert house_robber_recursive([2, 7, 9, 3, 1]) == 12
    assert target_sum_ways([1, 1, 1, 1, 1], 3) == 5

    assert len(subsets([1, 2, 3])) == 8
    assert len(subsets_with_duplicates([1, 2, 2])) == 6
    assert len(permutations([1, 2, 3])) == 6
    assert len(permutations_swap([1, 2, 3])) == 6
    assert len(permutations_with_duplicates([1, 1, 2])) == 3

    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum_ii(
        [10, 1, 2, 7, 6, 1, 5], 8
    ) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert combination_sum_iii(3, 7) == [[1, 2, 4]]

    assert len(letter_combinations("23")) == 9
    assert generate_parentheses(3) == [
        "((()))", "(()())", "(())()", "()(())", "()()()"
    ]

    assert palindrome_partition("aab") == [
        ["a", "a", "b"], ["aa", "b"]
    ]

    assert len(solve_n_queens(4)) == 2
    assert count_n_queens(4) == 2

    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    assert word_search(board, "ABCCED")

    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0],
        [1, 1, 1, 1]
    ]
    assert "DDRDRR" in rat_in_maze(maze)

    assert binary_strings(2) == ["00", "01", "10", "11"]
    assert binary_strings_no_consecutive_ones(3) == [
        "000", "001", "010", "100", "101"
    ]

    assert sorted(letter_case_permutation("a1b")) == sorted(
        ["a1b", "a1B", "A1b", "A1B"]
    )

    assert sorted(restore_ip_addresses("25525511135")) == sorted([
        "255.255.11.135",
        "255.255.111.35"
    ])

    assert combinations(4, 2) == [
        [1, 2], [1, 3], [1, 4],
        [2, 3], [2, 4], [3, 4]
    ]

    assert can_partition_k_subsets(
        [4, 3, 2, 3, 5, 2, 1], 4
    )

    print("All Recursion + Backtracking revision tests passed! ✓")


if __name__ == "__main__":
    print("=" * 70)
    print("RECURSION + BACKTRACKING — COMPLETE REVISION")
    print("=" * 70)
    print("Recursion fundamentals       ✓")
    print("Recursive arrays/search      ✓")
    print("Divide & conquer             ✓")
    print("Linked list recursion        ✓")
    print("Tree recursion               ✓")
    print("Memoized recursion / DP      ✓")
    print("Subsets                      ✓")
    print("Permutations                 ✓")
    print("Combinations                 ✓")
    print("String backtracking          ✓")
    print("Grid backtracking            ✓")
    print("N-Queens                     ✓")
    print("Sudoku                       ✓")
    print("Graph coloring               ✓")
    print("Partition problems           ✓")
    print("Pruning + templates          ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 70)

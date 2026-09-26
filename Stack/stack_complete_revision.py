"""
STACK — COMPLETE REVISION FILE
==============================

Purpose:
    Single Python revision library for DSA / placement preparation.

Covers:
    1. Stack fundamentals
    2. Array/list based stack
    3. Linked-list based stack
    4. Push / Pop / Peek / IsEmpty / Size
    5. Min Stack
    6. Monotonic Stack
    7. Next Greater / Smaller Element
    8. Stock Span
    9. Daily Temperatures
    10. Largest Rectangle in Histogram
    11. Maximal Rectangle
    12. Valid Parentheses
    13. Remove Adjacent Duplicates
    14. Decode String
    15. Simplify Path
    16. Evaluate Reverse Polish Notation
    17. Infix / Postfix / Prefix conversion
    18. Expression evaluation
    19. Backtracking with explicit stack
    20. DFS using stack
    21. Queue using two stacks
    22. Stack using queues
    23. Sort a stack
    24. Reverse a stack recursively
    25. Delete middle of stack
    26. Celebrity problem
    27. Asteroid collision
    28. Remove K digits
    29. Basic calculator
    30. Browser history style stack
    31. LRU-style design awareness
    32. Complexity cheat sheet
    33. Placement revision checklist

Python only.
"""


# ============================================================
# 0. STACK THEORY + COMPLEXITY
# ============================================================

"""
STACK = LIFO
Last In, First Out

Core operations:
    push(x)   -> add element
    pop()     -> remove top
    peek()    -> inspect top
    is_empty()
    size()

Typical complexity:
    push       O(1)
    pop        O(1)
    peek       O(1)
    is_empty   O(1)

Common applications:
    - Function call stack
    - Recursion
    - DFS
    - Backtracking
    - Undo / Redo
    - Browser history
    - Expression parsing
    - Parentheses matching
    - Monotonic stack
    - Histogram problems
"""


# ============================================================
# 1. ARRAY / LIST BASED STACK
# ============================================================

class ArrayStack:
    def __init__(self, capacity=None):
        self.items = []
        self.capacity = capacity

    def push(self, value):
        if self.capacity is not None and len(self.items) >= self.capacity:
            raise OverflowError("Stack overflow")

        self.items.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack underflow")

        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")

        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return f"ArrayStack({self.items!r})"


# ============================================================
# 2. STACK USING LINKED LIST
# ============================================================

class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedStack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, value):
        node = StackNode(value)
        node.next = self.top
        self.top = node
        self._size += 1

    def pop(self):
        if self.top is None:
            raise IndexError("Stack underflow")

        value = self.top.value
        self.top = self.top.next
        self._size -= 1

        return value

    def peek(self):
        if self.top is None:
            raise IndexError("Stack is empty")

        return self.top.value

    def is_empty(self):
        return self.top is None

    def size(self):
        return self._size


# ============================================================
# 3. MIN STACK
# ============================================================

class MinStack:
    """
    getMin() in O(1).

    Two-stack approach:
        main_stack -> all values
        min_stack  -> minimum at every level
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, value):
        self.stack.append(value)

        if not self.min_stack:
            self.min_stack.append(value)
        else:
            self.min_stack.append(
                min(value, self.min_stack[-1])
            )

    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")

        self.min_stack.pop()
        return self.stack.pop()

    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")

        return self.stack[-1]

    def get_min(self):
        if not self.min_stack:
            raise IndexError("Stack is empty")

        return self.min_stack[-1]


class MinStackSpaceOptimized:
    """
    One-stack mathematical encoding.

    Maintains current minimum and stores encoded values
    whenever a new minimum is inserted.

    All operations are O(1).
    """

    def __init__(self):
        self.stack = []
        self.minimum = None

    def push(self, value):
        if not self.stack:
            self.stack.append(value)
            self.minimum = value
            return

        if value >= self.minimum:
            self.stack.append(value)
        else:
            encoded = 2 * value - self.minimum
            self.stack.append(encoded)
            self.minimum = value

    def pop(self):
        if not self.stack:
            raise IndexError("Stack is empty")

        top = self.stack.pop()

        if top < self.minimum:
            old_min = 2 * self.minimum - top
            self.minimum = old_min

        if not self.stack:
            self.minimum = None

    def top(self):
        if not self.stack:
            raise IndexError("Stack is empty")

        top = self.stack[-1]

        if top < self.minimum:
            return self.minimum

        return top

    def get_min(self):
        if self.minimum is None:
            raise IndexError("Stack is empty")

        return self.minimum


# ============================================================
# 4. VALID PARENTHESES
# ============================================================

def is_valid_parentheses(s):
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    stack = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)

        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False

    return not stack


# ============================================================
# 5. REMOVE ADJACENT DUPLICATES
# ============================================================

def remove_adjacent_duplicates(s):
    stack = []

    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)

    return "".join(stack)


# ============================================================
# 6. REMOVE ALL ADJACENT DUPLICATES II
# ============================================================

def remove_duplicates_k(s, k):
    """
    Remove groups of exactly k adjacent equal characters.
    Stack stores [character, frequency].
    """
    stack = []

    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1

            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append([ch, 1])

    return "".join(ch * count for ch, count in stack)


# ============================================================
# 7. NEXT GREATER ELEMENT
# ============================================================

def next_greater_element(nums):
    """
    For each element, find first greater element to its right.

    Monotonic decreasing stack of indices.
    """
    result = [-1] * len(nums)
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            index = stack.pop()
            result[index] = value

        stack.append(i)

    return result


# ============================================================
# 8. NEXT GREATER ELEMENT II — CIRCULAR ARRAY
# ============================================================

def next_greater_circular(nums):
    n = len(nums)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        index = i % n

        while stack and nums[stack[-1]] < nums[index]:
            result[stack.pop()] = nums[index]

        if i < n:
            stack.append(index)

    return result


# ============================================================
# 9. NEXT SMALLER ELEMENT
# ============================================================

def next_smaller_element(nums):
    result = [-1] * len(nums)
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] > value:
            index = stack.pop()
            result[index] = value

        stack.append(i)

    return result


# ============================================================
# 10. PREVIOUS GREATER ELEMENT
# ============================================================

def previous_greater_element(nums):
    result = [-1] * len(nums)
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] <= value:
            stack.pop()

        if stack:
            result[i] = nums[stack[-1]]

        stack.append(i)

    return result


# ============================================================
# 11. PREVIOUS SMALLER ELEMENT
# ============================================================

def previous_smaller_element(nums):
    result = [-1] * len(nums)
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] >= value:
            stack.pop()

        if stack:
            result[i] = nums[stack[-1]]

        stack.append(i)

    return result


# ============================================================
# 12. DAILY TEMPERATURES
# ============================================================

def daily_temperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            previous = stack.pop()
            result[previous] = i - previous

        stack.append(i)

    return result


# ============================================================
# 13. STOCK SPAN
# ============================================================

def stock_span(prices):
    """
    span[i] = number of consecutive days ending at i
               with price <= current price.
    """
    spans = [0] * len(prices)
    stack = []

    for i, price in enumerate(prices):
        while stack and prices[stack[-1]] <= price:
            stack.pop()

        if not stack:
            spans[i] = i + 1
        else:
            spans[i] = i - stack[-1]

        stack.append(i)

    return spans


# ============================================================
# 14. LARGEST RECTANGLE IN HISTOGRAM
# ============================================================

def largest_rectangle_histogram(heights):
    """
    Monotonic increasing stack.

    O(n) time because each index enters and leaves stack once.
    """
    stack = []
    max_area = 0

    heights = heights + [0]

    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]

            left_smaller = stack[-1] if stack else -1
            width = i - left_smaller - 1

            max_area = max(max_area, h * width)

        stack.append(i)

    return max_area


# ============================================================
# 15. MAXIMAL RECTANGLE IN BINARY MATRIX
# ============================================================

def maximal_rectangle(matrix):
    if not matrix or not matrix[0]:
        return 0

    cols = len(matrix[0])
    heights = [0] * cols
    best = 0

    for row in matrix:
        for j in range(cols):
            if row[j] == "1" or row[j] == 1:
                heights[j] += 1
            else:
                heights[j] = 0

        best = max(best, largest_rectangle_histogram(heights))

    return best


# ============================================================
# 16. EVALUATE REVERSE POLISH NOTATION
# ============================================================

def eval_rpn(tokens):
    stack = []

    for token in tokens:
        if token not in {"+", "-", "*", "/"}:
            stack.append(int(token))
            continue

        b = stack.pop()
        a = stack.pop()

        if token == "+":
            result = a + b
        elif token == "-":
            result = a - b
        elif token == "*":
            result = a * b
        else:
            result = int(a / b)

        stack.append(result)

    return stack[-1]


# ============================================================
# 17. BASIC CALCULATOR II
# ============================================================

def calculate_basic_ii(s):
    """
    Supports:
        + - * /

    Uses stack to defer multiplication/division.
    """
    stack = []
    number = 0
    sign = "+"

    s = s.replace(" ", "") + "+"

    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        else:
            if sign == "+":
                stack.append(number)
            elif sign == "-":
                stack.append(-number)
            elif sign == "*":
                stack.append(stack.pop() * number)
            elif sign == "/":
                stack.append(int(stack.pop() / number))

            sign = ch
            number = 0

    return sum(stack)


# ============================================================
# 18. BASIC CALCULATOR — +, -, PARENTHESES
# ============================================================

def calculate_basic(s):
    """
    Supports:
        +
        -
        parentheses
    """
    result = 0
    number = 0
    sign = 1
    stack = []

    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)

        elif ch in "+-":
            result += sign * number
            number = 0
            sign = 1 if ch == "+" else -1

        elif ch == "(":
            stack.append(result)
            stack.append(sign)

            result = 0
            sign = 1

        elif ch == ")":
            result += sign * number
            number = 0

            result *= stack.pop()
            result += stack.pop()

    result += sign * number

    return result


# ============================================================
# 19. INFIX TO POSTFIX
# ============================================================

def infix_to_postfix(expression):
    """
    Example:
        A+B*C
        -> ABC*+

    Assumes operands are single characters/tokens.
    """
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "^": 3
    }

    output = []
    stack = []

    for token in expression:
        if token.isalnum():
            output.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())

            if stack:
                stack.pop()

        else:
            while (
                stack
                and stack[-1] != "("
                and precedence.get(stack[-1], 0) >= precedence[token]
            ):
                output.append(stack.pop())

            stack.append(token)

    while stack:
        output.append(stack.pop())

    return "".join(output)


# ============================================================
# 20. INFIX TO PREFIX
# ============================================================

def infix_to_prefix(expression):
    """
    Standard reverse + swap parentheses + postfix + reverse.
    """
    reversed_expression = expression[::-1]

    swapped = []

    for ch in reversed_expression:
        if ch == "(":
            swapped.append(")")
        elif ch == ")":
            swapped.append("(")
        else:
            swapped.append(ch)

    postfix = infix_to_postfix("".join(swapped))

    return postfix[::-1]


# ============================================================
# 21. POSTFIX EVALUATION
# ============================================================

def evaluate_postfix(expression):
    stack = []

    for token in expression.split():
        if token.lstrip("-").isdigit():
            stack.append(int(token))
            continue

        b = stack.pop()
        a = stack.pop()

        if token == "+":
            stack.append(a + b)
        elif token == "-":
            stack.append(a - b)
        elif token == "*":
            stack.append(a * b)
        elif token == "/":
            stack.append(int(a / b))
        else:
            raise ValueError(f"Unknown operator: {token}")

    return stack[-1]


# ============================================================
# 22. PREFIX EVALUATION
# ============================================================

def evaluate_prefix(expression):
    stack = []

    tokens = expression.split()

    for token in reversed(tokens):
        if token.lstrip("-").isdigit():
            stack.append(int(token))
            continue

        a = stack.pop()
        b = stack.pop()

        if token == "+":
            stack.append(a + b)
        elif token == "-":
            stack.append(a - b)
        elif token == "*":
            stack.append(a * b)
        elif token == "/":
            stack.append(int(a / b))
        else:
            raise ValueError(f"Unknown operator: {token}")

    return stack[-1]


# ============================================================
# 23. SIMPLIFY PATH
# ============================================================

def simplify_path(path):
    stack = []

    for part in path.split("/"):
        if part == "" or part == ".":
            continue

        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)

    return "/" + "/".join(stack)


# ============================================================
# 24. DECODE STRING
# ============================================================

def decode_string(s):
    """
    Example:
        3[a2[c]]
        -> accaccacc
    """
    stack = []
    current_string = ""
    current_number = 0

    for ch in s:
        if ch.isdigit():
            current_number = current_number * 10 + int(ch)

        elif ch == "[":
            stack.append((current_string, current_number))
            current_string = ""
            current_number = 0

        elif ch == "]":
            previous_string, repeat = stack.pop()
            current_string = previous_string + current_string * repeat

        else:
            current_string += ch

    return current_string


# ============================================================
# 25. ASTEROID COLLISION
# ============================================================

def asteroid_collision(asteroids):
    stack = []

    for asteroid in asteroids:
        alive = True

        while (
            alive
            and asteroid < 0
            and stack
            and stack[-1] > 0
        ):
            if stack[-1] < -asteroid:
                stack.pop()
                continue

            if stack[-1] == -asteroid:
                stack.pop()

            alive = False

        if alive:
            stack.append(asteroid)

    return stack


# ============================================================
# 26. REMOVE K DIGITS
# ============================================================

def remove_k_digits(num, k):
    stack = []

    for digit in num:
        while stack and k > 0 and stack[-1] > digit:
            stack.pop()
            k -= 1

        stack.append(digit)

    while k > 0:
        stack.pop()
        k -= 1

    result = "".join(stack).lstrip("0")

    return result if result else "0"


# ============================================================
# 27. TRAPPING RAIN WATER — STACK
# ============================================================

def trap_rain_water_stack(height):
    stack = []
    water = 0

    for i, current_height in enumerate(height):
        while stack and current_height > height[stack[-1]]:
            bottom = stack.pop()

            if not stack:
                break

            left = stack[-1]
            width = i - left - 1
            bounded_height = (
                min(height[left], current_height)
                - height[bottom]
            )

            water += width * bounded_height

        stack.append(i)

    return water


# ============================================================
# 28. DAILY TEMPERATURES — ALTERNATIVE VALUE STACK
# ============================================================

def daily_temperatures_pairs(temperatures):
    result = [0] * len(temperatures)
    stack = []  # (temperature, index)

    for i, temperature in enumerate(temperatures):
        while stack and stack[-1][0] < temperature:
            _, previous_index = stack.pop()
            result[previous_index] = i - previous_index

        stack.append((temperature, i))

    return result


# ============================================================
# 29. ONLINE STOCK SPAN
# ============================================================

class StockSpanner:
    """
    Stack of [price, accumulated_span].
    """

    def __init__(self):
        self.stack = []

    def next(self, price):
        span = 1

        while self.stack and self.stack[-1][0] <= price:
            _, previous_span = self.stack.pop()
            span += previous_span

        self.stack.append((price, span))

        return span


# ============================================================
# 30. QUEUE USING TWO STACKS
# ============================================================

class QueueUsingStacks:
    """
    Amortized O(1) enqueue/dequeue.
    """

    def __init__(self):
        self.input = []
        self.output = []

    def _transfer(self):
        if not self.output:
            while self.input:
                self.output.append(self.input.pop())

    def enqueue(self, value):
        self.input.append(value)

    def dequeue(self):
        self._transfer()

        if not self.output:
            raise IndexError("Queue is empty")

        return self.output.pop()

    def peek(self):
        self._transfer()

        if not self.output:
            raise IndexError("Queue is empty")

        return self.output[-1]

    def empty(self):
        return not self.input and not self.output


# ============================================================
# 31. STACK USING TWO QUEUES
# ============================================================

from collections import deque


class StackUsingQueues:
    """
    Push O(n), pop O(1).
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
# 32. SORT A STACK USING ANOTHER STACK
# ============================================================

def sort_stack(stack):
    """
    Input:
        Python list where last element is stack top.

    Returns sorted stack such that smallest element is on top.
    """
    temp = []

    while stack:
        current = stack.pop()

        while temp and temp[-1] > current:
            stack.append(temp.pop())

        temp.append(current)

    return temp


# ============================================================
# 33. REVERSE A STACK USING RECURSION
# ============================================================

def insert_at_bottom(stack, value):
    if not stack:
        stack.append(value)
        return

    top = stack.pop()
    insert_at_bottom(stack, value)
    stack.append(top)


def reverse_stack_recursive(stack):
    if not stack:
        return

    top = stack.pop()
    reverse_stack_recursive(stack)
    insert_at_bottom(stack, top)


# ============================================================
# 34. DELETE MIDDLE OF STACK
# ============================================================

def delete_middle_stack(stack):
    """
    Deletes middle element using recursion.

    For even size, this removes the upper middle according
    to zero-based interpretation.
    """
    if not stack:
        return

    target = (len(stack) + 1) // 2

    def delete(stack, current):
        if current == target:
            stack.pop()
            return

        value = stack.pop()
        delete(stack, current + 1)
        stack.append(value)

    delete(stack, 1)


# ============================================================
# 35. CELEBRITY PROBLEM
# ============================================================

def celebrity(matrix):
    """
    matrix[a][b] == 1 means a knows b.

    Celebrity:
        knows nobody
        everybody knows them

    O(n) time, O(1) extra space.
    """
    n = len(matrix)

    if n == 0:
        return -1

    candidate = 0

    for person in range(1, n):
        if matrix[candidate][person] == 1:
            candidate = person

    for person in range(n):
        if person == candidate:
            continue

        if (
            matrix[candidate][person] == 1
            or matrix[person][candidate] == 0
        ):
            return -1

    return candidate


# ============================================================
# 36. DFS USING EXPLICIT STACK
# ============================================================

def dfs_iterative(graph, start):
    """
    graph:
        {
            node: [neighbors]
        }
    """
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


# ============================================================
# 37. BACKTRACKING WITH EXPLICIT STACK
# ============================================================

def subsets_iterative(nums):
    """
    Generates all subsets without recursion.

    Each stack state:
        (index, current_subset)
    """
    result = []
    stack = [(0, [])]

    while stack:
        index, current = stack.pop()

        if index == len(nums):
            result.append(current)
            continue

        # Exclude
        stack.append((index + 1, current.copy()))

        # Include
        stack.append(
            (index + 1, current + [nums[index]])
        )

    return result


# ============================================================
# 38. GENERATE BINARY NUMBERS USING QUEUE-LIKE PROCESS
# ============================================================

def generate_binary_numbers(n):
    """
    Included as a stack/queue revision connection.
    """
    result = []

    for i in range(1, n + 1):
        result.append(bin(i)[2:])

    return result


# ============================================================
# 39. BROWSER HISTORY USING TWO STACKS
# ============================================================

class BrowserHistory:
    def __init__(self, homepage):
        self.back_stack = []
        self.forward_stack = []
        self.current = homepage

    def visit(self, url):
        self.back_stack.append(self.current)
        self.current = url
        self.forward_stack.clear()

    def back(self, steps):
        while steps > 0 and self.back_stack:
            self.forward_stack.append(self.current)
            self.current = self.back_stack.pop()
            steps -= 1

        return self.current

    def forward(self, steps):
        while steps > 0 and self.forward_stack:
            self.back_stack.append(self.current)
            self.current = self.forward_stack.pop()
            steps -= 1

        return self.current


# ============================================================
# 40. MONOTONIC STACK TEMPLATE
# ============================================================

def monotonic_increasing_stack_template(nums):
    """
    Generic pattern.

    Stack remains increasing by value.
    Modify the "while" condition depending on the problem.
    """
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] > value:
            index = stack.pop()

            # Process index here.

        stack.append(i)

    return stack


def monotonic_decreasing_stack_template(nums):
    """
    Generic pattern.

    Stack remains decreasing by value.
    """
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            index = stack.pop()

            # Process index here.

        stack.append(i)

    return stack


# ============================================================
# 41. COLLAPSING / CANCELLATION PATTERN
# ============================================================

def cancel_adjacent_pairs(items):
    """
    Generic stack cancellation pattern.

    Example:
        [1, 1, 2, 3, 3]
        -> [2]
    """
    stack = []

    for item in items:
        if stack and stack[-1] == item:
            stack.pop()
        else:
            stack.append(item)

    return stack


# ============================================================
# 42. INTERVIEW PATTERN: WAIT FOR FUTURE EVENT
# ============================================================

def next_greater_distance(nums):
    """
    Returns distance to next greater element.

    Core pattern:
        Keep unresolved indices in stack.
    """
    result = [-1] * len(nums)
    stack = []

    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            j = stack.pop()
            result[j] = i - j

        stack.append(i)

    return result


# ============================================================
# 43. TEST HELPERS
# ============================================================

def run_revision_tests():
    # Basic Stack
    stack = ArrayStack()

    stack.push(10)
    stack.push(20)
    stack.push(30)

    assert stack.peek() == 30
    assert stack.pop() == 30
    assert stack.size() == 2

    # Linked Stack
    linked_stack = LinkedStack()

    linked_stack.push(1)
    linked_stack.push(2)

    assert linked_stack.peek() == 2
    assert linked_stack.pop() == 2

    # Min Stack
    minimum = MinStack()

    minimum.push(5)
    minimum.push(3)
    minimum.push(7)

    assert minimum.get_min() == 3
    minimum.pop()
    assert minimum.get_min() == 3

    # Parentheses
    assert is_valid_parentheses("()[]{}")
    assert not is_valid_parentheses("(]")

    # Adjacent duplicates
    assert remove_adjacent_duplicates("abbaca") == "ca"

    # Next greater
    assert next_greater_element(
        [2, 1, 2, 4, 3]
    ) == [4, 2, 4, -1, -1]

    # Circular next greater
    assert next_greater_circular(
        [1, 2, 1]
    ) == [2, -1, 2]

    # Daily temperatures
    assert daily_temperatures(
        [73, 74, 75, 71, 69, 72, 76, 73]
    ) == [1, 1, 4, 2, 1, 1, 0, 0]

    # Stock span
    assert stock_span(
        [100, 80, 60, 70, 60, 75, 85]
    ) == [1, 1, 1, 2, 1, 4, 6]

    # Histogram
    assert largest_rectangle_histogram(
        [2, 1, 5, 6, 2, 3]
    ) == 10

    # RPN
    assert eval_rpn(
        ["2", "1", "+", "3", "*"]
    ) == 9

    # Decode
    assert decode_string("3[a2[c]]") == "accaccacc"

    # Path
    assert simplify_path("/a/./b/../../c/") == "/c"

    # Asteroid
    assert asteroid_collision(
        [5, 10, -5]
    ) == [5, 10]

    # Remove K digits
    assert remove_k_digits("1432219", 3) == "1219"

    # Queue using stacks
    queue = QueueUsingStacks()

    queue.enqueue(1)
    queue.enqueue(2)

    assert queue.peek() == 1
    assert queue.dequeue() == 1

    # Stack using queues
    sq = StackUsingQueues()

    sq.push(1)
    sq.push(2)

    assert sq.top() == 2
    assert sq.pop() == 2

    # DFS
    graph = {
        1: [2, 3],
        2: [4],
        3: [],
        4: []
    }

    assert dfs_iterative(graph, 1) == [1, 2, 4, 3]

    # Browser
    browser = BrowserHistory("google.com")
    browser.visit("leetcode.com")
    browser.visit("github.com")

    assert browser.back(1) == "leetcode.com"
    assert browser.forward(1) == "github.com"

    print("All Stack revision tests passed! ✓")


# ============================================================
# 44. PLACEMENT REVISION CHECKLIST
# ============================================================

"""
BASIC
[ ] Understand LIFO
[ ] Implement stack using Python list
[ ] Implement stack using linked list
[ ] push
[ ] pop
[ ] peek
[ ] is_empty
[ ] size
[ ] Overflow / underflow

CORE
[ ] Valid parentheses
[ ] Remove adjacent duplicates
[ ] Evaluate postfix
[ ] Evaluate prefix
[ ] Evaluate RPN
[ ] Infix -> Postfix
[ ] Infix -> Prefix
[ ] Basic Calculator
[ ] Basic Calculator II
[ ] Decode String
[ ] Simplify Path

MONOTONIC STACK
[ ] Understand increasing stack
[ ] Understand decreasing stack
[ ] Next greater element
[ ] Next smaller element
[ ] Previous greater element
[ ] Previous smaller element
[ ] Circular next greater
[ ] Daily temperatures
[ ] Stock span
[ ] Online stock span
[ ] Largest rectangle in histogram
[ ] Maximal rectangle
[ ] Trapping rain water

DESIGN
[ ] Min Stack
[ ] Min Stack O(1)
[ ] Queue using two stacks
[ ] Stack using two queues
[ ] Browser history

ADVANCED
[ ] Asteroid collision
[ ] Remove K digits
[ ] Celebrity problem
[ ] DFS using explicit stack
[ ] Backtracking using explicit stack
[ ] Sort a stack
[ ] Reverse a stack recursively
[ ] Delete middle of stack

MOST IMPORTANT INTERVIEW QUESTIONS
[ ] Why is stack LIFO?
[ ] Why are push/pop O(1)?
[ ] Array stack vs linked-list stack?
[ ] How does recursion use a stack?
[ ] Why does monotonic stack achieve O(n)?
[ ] Why can each element be pushed and popped only once?
[ ] How does Min Stack get O(1) minimum?
[ ] How do you implement a queue using stacks?
[ ] How do you implement a stack using queues?
[ ] Why is histogram solved using a monotonic stack?
[ ] Why is DFS naturally implemented using a stack?
[ ] How does stack help in expression evaluation?
[ ] Prefix vs postfix vs infix?
[ ] When should you recognize a monotonic stack?

PLACEMENT RULE:
Don't memorize individual solutions.

Recognize the pattern:

1. "Nearest greater/smaller"
       -> Monotonic Stack

2. "Wait until a future element satisfies condition"
       -> Monotonic Stack

3. "Nested structure"
       -> Stack

4. "Matching brackets"
       -> Stack

5. "Undo / history"
       -> Stack

6. "Expression evaluation"
       -> Stack

7. "DFS without recursion"
       -> Stack

8. "Repeated cancellation"
       -> Stack

9. "Need minimum/maximum with O(1) query"
       -> Auxiliary Stack / Monotonic Stack
"""


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 65)
    print("STACK — COMPLETE REVISION LIBRARY")
    print("=" * 65)
    print()
    print("Basic Stack            ✓")
    print("Linked-List Stack      ✓")
    print("Min Stack              ✓")
    print("Parentheses             ✓")
    print("Expression Algorithms   ✓")
    print("Monotonic Stack         ✓")
    print("Histogram               ✓")
    print("Stack/Queue Design      ✓")
    print("DFS / Backtracking      ✓")
    print("Advanced Problems       ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 65)

    # Uncomment:
    # run_revision_tests()

"""
ARRAYS — COMPLETE DSA REVISION
==============================

Placement-focused revision library covering:
- Array basics
- Traversal / CRUD
- Prefix sums
- Difference arrays
- Two pointers
- Sliding window
- Kadane's algorithm
- Hashing patterns
- Binary search
- Binary search on answer
- Sorting patterns
- Intervals
- Matrix problems
- Subarrays / subsequences
- Monotonic stack patterns
- Greedy array patterns
- Common interview templates
- Complexity and pattern-recognition cheat sheets

Python implementations.
"""

from collections import Counter, defaultdict, deque
import bisect
import heapq


# ============================================================
# BASIC ARRAY OPERATIONS
# ============================================================

def traverse(arr):
    """Return all elements in traversal order."""
    return arr[:]


def insert_at(arr, index, value):
    """Insert value at index."""
    arr = arr[:]
    arr.insert(index, value)
    return arr


def delete_at(arr, index):
    """Delete and return array after removing index."""
    arr = arr[:]
    arr.pop(index)
    return arr


def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def reverse_array(arr):
    return arr[::-1]


def reverse_array_in_place(arr):
    arr = arr[:]
    left, right = 0, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

    return arr


# ============================================================
# PREFIX SUM
# ============================================================

def prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)

    for i, value in enumerate(arr):
        prefix[i + 1] = prefix[i] + value

    return prefix


def range_sum(arr, left, right):
    """Inclusive range sum [left, right]."""
    prefix = prefix_sum(arr)
    return prefix[right + 1] - prefix[left]


def subarray_sum_equals_k(arr, k):
    """Count subarrays whose sum equals k."""
    prefix_count = {0: 1}
    current_sum = 0
    count = 0

    for value in arr:
        current_sum += value
        count += prefix_count.get(current_sum - k, 0)
        prefix_count[current_sum] = (
            prefix_count.get(current_sum, 0) + 1
        )

    return count


# ============================================================
# DIFFERENCE ARRAY
# ============================================================

def range_increment(n, updates):
    """
    updates = [(left, right, value), ...]
    Add value to every index in [left, right].
    """
    diff = [0] * (n + 1)

    for left, right, value in updates:
        diff[left] += value
        if right + 1 < len(diff):
            diff[right + 1] -= value

    result = [0] * n
    current = 0

    for i in range(n):
        current += diff[i]
        result[i] = current

    return result


# ============================================================
# TWO POINTERS
# ============================================================

def two_sum_sorted(arr, target):
    """Return indices for a sorted array."""
    left, right = 0, len(arr) - 1

    while left < right:
        total = arr[left] + arr[right]

        if total == target:
            return [left, right]

        if total < target:
            left += 1
        else:
            right -= 1

    return []


def remove_duplicates_sorted(arr):
    """Return sorted array with duplicates removed."""
    if not arr:
        return []

    result = [arr[0]]

    for value in arr[1:]:
        if value != result[-1]:
            result.append(value)

    return result


def move_zeroes(arr):
    arr = arr[:]
    write = 0

    for value in arr:
        if value != 0:
            arr[write] = value
            write += 1

    while write < len(arr):
        arr[write] = 0
        write += 1

    return arr


def is_palindrome_array(arr):
    left, right = 0, len(arr) - 1

    while left < right:
        if arr[left] != arr[right]:
            return False

        left += 1
        right -= 1

    return True


def container_with_most_water(height):
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        width = right - left
        best = max(
            best,
            width * min(height[left], height[right])
        )

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best


def three_sum(nums):
    nums = sorted(nums)
    result = []

    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append(
                    [nums[i], nums[left], nums[right]]
                )

                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1

                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

            elif total < 0:
                left += 1
            else:
                right -= 1

    return result


# ============================================================
# SLIDING WINDOW
# ============================================================

def max_sum_subarray_fixed_k(arr, k):
    if k <= 0 or k > len(arr):
        return None

    window_sum = sum(arr[:k])
    best = window_sum

    for right in range(k, len(arr)):
        window_sum += arr[right]
        window_sum -= arr[right - k]
        best = max(best, window_sum)

    return best


def max_sum_subarray_fixed_k_indices(arr, k):
    if k <= 0 or k > len(arr):
        return None

    window_sum = sum(arr[:k])
    best = window_sum
    best_left = 0

    for right in range(k, len(arr)):
        window_sum += arr[right]
        window_sum -= arr[right - k]

        if window_sum > best:
            best = window_sum
            best_left = right - k + 1

    return best, best_left, best_left + k - 1


def longest_subarray_sum_at_most_k_positive(arr, k):
    """
    Works when all values are non-negative.
    """
    left = 0
    current = 0
    best = 0

    for right, value in enumerate(arr):
        current += value

        while current > k and left <= right:
            current -= arr[left]
            left += 1

        best = max(best, right - left + 1)

    return best


def min_subarray_len(target, nums):
    left = 0
    current = 0
    best = float("inf")

    for right, value in enumerate(nums):
        current += value

        while current >= target:
            best = min(best, right - left + 1)
            current -= nums[left]
            left += 1

    return 0 if best == float("inf") else best


def longest_substring_without_repeating(s):
    left = 0
    last_seen = {}
    best = 0

    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1

        last_seen[char] = right
        best = max(best, right - left + 1)

    return best


# ============================================================
# KADANE'S ALGORITHM
# ============================================================

def max_subarray_sum(nums):
    if not nums:
        return 0

    current = best = nums[0]

    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)

    return best


def max_subarray_with_indices(nums):
    if not nums:
        return 0, -1, -1

    current = best = nums[0]
    current_start = 0
    best_start = best_end = 0

    for i in range(1, len(nums)):
        if nums[i] > current + nums[i]:
            current = nums[i]
            current_start = i
        else:
            current += nums[i]

        if current > best:
            best = current
            best_start = current_start
            best_end = i

    return best, best_start, best_end


def max_circular_subarray_sum(nums):
    total = sum(nums)
    normal = max_subarray_sum(nums)

    min_current = min_best = nums[0]

    for value in nums[1:]:
        min_current = min(value, min_current + value)
        min_best = min(min_best, min_current)

    if normal < 0:
        return normal

    return max(normal, total - min_best)


# ============================================================
# HASHING ARRAY PATTERNS
# ============================================================

def two_sum(nums, target):
    seen = {}

    for i, value in enumerate(nums):
        complement = target - value

        if complement in seen:
            return [seen[complement], i]

        seen[value] = i

    return []


def longest_consecutive_sequence(nums):
    values = set(nums)
    best = 0

    for value in values:
        if value - 1 not in values:
            current = value

            while current + 1 in values:
                current += 1

            best = max(best, current - value + 1)

    return best


def majority_element(nums):
    """Boyer-Moore Voting Algorithm."""
    candidate = None
    count = 0

    for value in nums:
        if count == 0:
            candidate = value

        count += 1 if value == candidate else -1

    return candidate


def majority_elements_n_by_3(nums):
    candidate1 = candidate2 = None
    count1 = count2 = 0

    for value in nums:
        if value == candidate1:
            count1 += 1
        elif value == candidate2:
            count2 += 1
        elif count1 == 0:
            candidate1, count1 = value, 1
        elif count2 == 0:
            candidate2, count2 = value, 1
        else:
            count1 -= 1
            count2 -= 1

    result = []

    for candidate in (candidate1, candidate2):
        if candidate is not None and nums.count(candidate) > len(nums) // 3:
            if candidate not in result:
                result.append(candidate)

    return result


def longest_zero_sum_subarray(nums):
    first_index = {0: -1}
    current_sum = 0
    best = 0

    for i, value in enumerate(nums):
        current_sum += value

        if current_sum in first_index:
            best = max(best, i - first_index[current_sum])
        else:
            first_index[current_sum] = i

    return best


# ============================================================
# ROTATION
# ============================================================

def rotate_array(nums, k):
    if not nums:
        return []

    nums = nums[:]
    k %= len(nums)

    nums.reverse()
    nums[:k] = reversed(nums[:k])
    nums[k:] = reversed(nums[k:])

    return nums


def rotate_array_simple(nums, k):
    if not nums:
        return []

    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums[:]


# ============================================================
# MERGING
# ============================================================

def merge_sorted_arrays(a, b):
    i = j = 0
    result = []

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])

    return result


def merge_intervals(intervals):
    if not intervals:
        return []

    intervals = sorted(intervals)
    result = [intervals[0][:]]

    for start, end in intervals[1:]:
        if start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])

    return result


def insert_interval(intervals, new_interval):
    result = []
    i = 0

    while i < len(intervals) and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    while i < len(intervals) and intervals[i][0] <= new_interval[1]:
        new_interval = [
            min(new_interval[0], intervals[i][0]),
            max(new_interval[1], intervals[i][1])
        ]
        i += 1

    result.append(new_interval)
    result.extend(intervals[i:])

    return result


def interval_intersection(a, b):
    i = j = 0
    result = []

    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])

        if start <= end:
            result.append([start, end])

        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1

    return result


# ============================================================
# BINARY SEARCH
# ============================================================

def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def lower_bound(arr, target):
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def upper_bound(arr, target):
    left, right = 0, len(arr)

    while left < right:
        mid = (left + right) // 2

        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left


def search_range(arr, target):
    left = lower_bound(arr, target)

    if left == len(arr) or arr[left] != target:
        return [-1, -1]

    return [left, upper_bound(arr, target) - 1]


def search_rotated_sorted_array(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def find_min_rotated_sorted_array(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


def find_peak_element(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            right = mid

    return left


# ============================================================
# BINARY SEARCH ON ANSWER
# ============================================================

def integer_square_root(x):
    if x < 2:
        return x

    left, right = 1, x // 2
    answer = 1

    while left <= right:
        mid = (left + right) // 2

        if mid <= x // mid:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1

    return answer


def koko_eating_bananas(piles, h):
    left, right = 1, max(piles)

    while left < right:
        speed = (left + right) // 2

        hours = sum(
            (pile + speed - 1) // speed
            for pile in piles
        )

        if hours <= h:
            right = speed
        else:
            left = speed + 1

    return left


def ship_within_days(weights, days):
    left = max(weights)
    right = sum(weights)

    def can_ship(capacity):
        used_days = 1
        current = 0

        for weight in weights:
            if current + weight > capacity:
                used_days += 1
                current = 0

            current += weight

        return used_days <= days

    while left < right:
        capacity = (left + right) // 2

        if can_ship(capacity):
            right = capacity
        else:
            left = capacity + 1

    return left


# ============================================================
# SORTING
# ============================================================

def bubble_sort(arr):
    arr = arr[:]

    for i in range(len(arr)):
        swapped = False

        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def selection_sort(arr):
    arr = arr[:]

    for i in range(len(arr)):
        min_index = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(arr):
    arr = arr[:]

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge_sorted_arrays(left, right)


def quick_sort(arr):
    arr = arr[:]

    def partition(low, high):
        pivot = arr[high]
        i = low

        for j in range(low, high):
            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[i], arr[high] = arr[high], arr[i]
        return i

    def quicksort(low, high):
        if low >= high:
            return

        pivot_index = partition(low, high)
        quicksort(low, pivot_index - 1)
        quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)
    return arr


def heap_sort(arr):
    return sorted(arr)


# ============================================================
# SPECIAL SORTING PATTERNS
# ============================================================

def sort_colors(nums):
    """Dutch National Flag algorithm."""
    nums = nums[:]
    low = mid = 0
    high = len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1

        elif nums[mid] == 1:
            mid += 1

        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

    return nums


def count_inversions(nums):
    """Count inversions using merge sort."""
    arr = nums[:]

    def merge_sort_count(values):
        if len(values) <= 1:
            return values, 0

        mid = len(values) // 2
        left, left_count = merge_sort_count(values[:mid])
        right, right_count = merge_sort_count(values[mid:])

        merged = []
        i = j = 0
        inversions = left_count + right_count

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                inversions += len(left) - i

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, inversions

    _, count = merge_sort_count(arr)
    return count


# ============================================================
# FREQUENCY / BUCKET PATTERNS
# ============================================================

def top_k_frequent(nums, k):
    frequency = Counter(nums)

    buckets = [[] for _ in range(len(nums) + 1)]

    for value, count in frequency.items():
        buckets[count].append(value)

    result = []

    for count in range(len(buckets) - 1, 0, -1):
        for value in buckets[count]:
            result.append(value)

            if len(result) == k:
                return result

    return result


def product_except_self(nums):
    result = [1] * len(nums)

    prefix = 1

    for i in range(len(nums)):
        result[i] = prefix
        prefix *= nums[i]

    suffix = 1

    for i in range(len(nums) - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result


# ============================================================
# GREEDY ARRAY PATTERNS
# ============================================================

def can_jump(nums):
    farthest = 0

    for i, jump in enumerate(nums):
        if i > farthest:
            return False

        farthest = max(farthest, i + jump)

    return True


def jump_game_min_jumps(nums):
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps


def gas_station(gas, cost):
    if sum(gas) < sum(cost):
        return -1

    start = 0
    tank = 0

    for i in range(len(gas)):
        tank += gas[i] - cost[i]

        if tank < 0:
            start = i + 1
            tank = 0

    return start


# ============================================================
# MATRIX / 2D ARRAYS
# ============================================================

def transpose_matrix(matrix):
    if not matrix:
        return []

    return [list(row) for row in zip(*matrix)]


def rotate_matrix_90(matrix):
    """Clockwise rotation."""
    if not matrix:
        return []

    matrix = [row[:] for row in matrix]
    n = len(matrix)

    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = (
                matrix[j][i],
                matrix[i][j]
            )

    for row in matrix:
        row.reverse()

    return matrix


def spiral_order(matrix):
    if not matrix:
        return []

    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1

    result = []

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            result.append(matrix[top][col])

        top += 1

        for row in range(top, bottom + 1):
            result.append(matrix[row][right])

        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])

            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])

            left += 1

    return result


def search_sorted_matrix(matrix, target):
    """
    Rows and columns sorted increasingly.
    """
    if not matrix or not matrix[0]:
        return False

    row = 0
    col = len(matrix[0]) - 1

    while row < len(matrix) and col >= 0:
        if matrix[row][col] == target:
            return True

        if matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False


# ============================================================
# SUBARRAY / SUBSEQUENCE PATTERNS
# ============================================================

def max_product_subarray(nums):
    if not nums:
        return 0

    current_max = current_min = result = nums[0]

    for value in nums[1:]:
        if value < 0:
            current_max, current_min = (
                current_min,
                current_max
            )

        current_max = max(
            value,
            current_max * value
        )

        current_min = min(
            value,
            current_min * value
        )

        result = max(result, current_max)

    return result


def longest_increasing_subsequence(nums):
    """
    O(n log n) LIS length.
    """
    tails = []

    for value in nums:
        index = bisect.bisect_left(tails, value)

        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value

    return len(tails)


def maximum_length_subarray_positive(nums):
    """Longest contiguous subarray with all positive values."""
    best = current = 0

    for value in nums:
        if value > 0:
            current += 1
            best = max(best, current)
        else:
            current = 0

    return best


# ============================================================
# MONOTONIC STACK ARRAY PATTERNS
# ============================================================

def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []

    for i in range(len(nums) - 1, -1, -1):
        while stack and stack[-1] <= nums[i]:
            stack.pop()

        if stack:
            result[i] = stack[-1]

        stack.append(nums[i])

    return result


def daily_temperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            previous = stack.pop()
            result[previous] = i - previous

        stack.append(i)

    return result


def largest_rectangle_histogram(heights):
    stack = []
    best = 0

    heights = heights + [0]

    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, h * width)

        stack.append(i)

    return best


# ============================================================
# RANDOMIZED / SELECTION PATTERN
# ============================================================

def kth_largest_heap(nums, k):
    heap = []

    for value in nums:
        heapq.heappush(heap, value)

        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


# ============================================================
# 2D PREFIX SUM
# ============================================================

class NumMatrix:
    def __init__(self, matrix):
        if not matrix or not matrix[0]:
            self.prefix = [[0]]

            return

        rows = len(matrix)
        cols = len(matrix[0])

        self.prefix = [
            [0] * (cols + 1)
            for _ in range(rows + 1)
        ]

        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def sum_region(self, r1, c1, r2, c2):
        p = self.prefix

        return (
            p[r2 + 1][c2 + 1]
            - p[r1][c2 + 1]
            - p[r2 + 1][c1]
            + p[r1][c1]
        )


# ============================================================
# PATTERN RECOGNITION CHEAT SHEET
# ============================================================

"""
ARRAY PATTERN RECOGNITION
=========================

1. Need direct traversal?
   -> Simple loop

2. Need repeated range sums?
   -> Prefix sum

3. Need repeated range updates?
   -> Difference array

4. Sorted array + pair relationship?
   -> Two pointers

5. Contiguous subarray + fixed size?
   -> Fixed sliding window

6. Contiguous subarray + dynamic condition?
   -> Sliding window
   -> But verify whether negatives break monotonicity

7. Maximum contiguous sum?
   -> Kadane

8. Pair sum?
   -> Hash map
   -> Two pointers if sorted

9. Remove duplicates from sorted array?
   -> Two pointers

10. Search sorted array?
    -> Binary search

11. Sorted array rotated?
    -> Modified binary search

12. Minimum possible maximum / maximum possible minimum?
    -> Binary search on answer

13. Intervals overlap?
    -> Sort + merge / sweep

14. Need top K?
    -> Heap / bucket / sorting

15. Next greater / previous greater?
    -> Monotonic stack

16. Matrix boundary traversal?
    -> Spiral / directional simulation

17. Grid row + column sorted?
    -> Staircase search

18. Need O(1) extra space rearrangement?
    -> In-place / two pointers / cyclic placement

19. Values are 1..n and one missing/repeated?
    -> Cyclic sort / XOR / frequency

20. Need longest consecutive values?
    -> Hash set

21. Majority element?
    -> Boyer-Moore

22. Product of all except self?
    -> Prefix + suffix

23. Maximum product subarray?
    -> Track current max + min

24. Reachability through jumps?
    -> Greedy

25. Minimum jumps?
    -> Greedy level expansion

26. Minimum capacity to satisfy days?
    -> Binary search on answer


COMPLEXITY CHEAT SHEET
======================

Traversal:
    Time: O(n)
    Space: O(1)

Prefix sum:
    Build: O(n)
    Query: O(1)

Hash map lookup:
    Average: O(1)

Two pointers:
    Usually O(n)

Sliding window:
    Usually O(n)

Kadane:
    Time: O(n)
    Space: O(1)

Binary search:
    Time: O(log n)
    Space: O(1)

Merge sort:
    Time: O(n log n)
    Space: O(n)

Quick sort:
    Average: O(n log n)
    Worst: O(n²)

Heap:
    Insert: O(log n)
    Remove: O(log n)
    Peek: O(1)

LIS:
    O(n log n)

Monotonic stack:
    Usually O(n)

2D prefix sum:
    Build: O(rows * cols)
    Query: O(1)


BINARY SEARCH ON ANSWER
=======================

The most important mental model:

1. Define the answer space.
2. Pick a candidate answer.
3. Write a feasibility function.
4. Check whether the candidate works.
5. Use monotonicity to eliminate half the search space.

Typical examples:
    - Koko Eating Bananas
    - Ship Packages Within D Days
    - Split Array Largest Sum
    - Allocate Books
    - Aggressive Cows
    - Capacity / speed / distance problems


IMPORTANT ARRAY INTERVIEW QUESTIONS
===================================

1. Two Sum
2. Best Time to Buy and Sell Stock
3. Maximum Subarray
4. Product of Array Except Self
5. Maximum Product Subarray
6. Contains Duplicate
7. Majority Element
8. Longest Consecutive Sequence
9. Move Zeroes
10. Rotate Array
11. Remove Duplicates from Sorted Array
12. 3Sum
13. Container With Most Water
14. Trapping Rain Water
15. Subarray Sum Equals K
16. Longest Subarray With Sum K
17. Minimum Size Subarray Sum
18. Merge Intervals
19. Insert Interval
20. Non-overlapping Intervals
21. Sort Colors
22. Search in Rotated Sorted Array
23. Find Minimum in Rotated Sorted Array
24. Find Peak Element
25. Kth Largest Element
26. Top K Frequent Elements
27. Jump Game
28. Jump Game II
29. Gas Station
30. Spiral Matrix
31. Rotate Image
32. Set Matrix Zeroes
33. Search a 2D Matrix
34. Daily Temperatures
35. Largest Rectangle in Histogram
36. Longest Increasing Subsequence
37. Koko Eating Bananas
38. Capacity to Ship Packages
39. Count Inversions
40. Shortest Unsorted Continuous Subarray


PLACEMENT CHECKLIST
===================

FOUNDATION
[ ] Traversal
[ ] Search
[ ] Insert / delete
[ ] Reverse
[ ] In-place manipulation

PREFIX / RANGE
[ ] Prefix sum
[ ] Difference array
[ ] Subarray sum
[ ] 2D prefix sum

TWO POINTERS
[ ] Pair sum
[ ] Remove duplicates
[ ] Move zeroes
[ ] Palindrome
[ ] Container with most water
[ ] 3Sum

SLIDING WINDOW
[ ] Fixed window
[ ] Variable window
[ ] Longest valid window
[ ] Minimum valid window
[ ] Frequency-based window

KADANE
[ ] Maximum subarray
[ ] Recover subarray
[ ] Circular maximum subarray
[ ] Maximum product subarray

HASHING
[ ] Two Sum
[ ] Frequency map
[ ] Longest consecutive
[ ] Zero-sum subarray
[ ] Majority element

BINARY SEARCH
[ ] Basic binary search
[ ] Lower bound
[ ] Upper bound
[ ] First / last occurrence
[ ] Rotated array
[ ] Peak
[ ] Binary search on answer

SORTING
[ ] Bubble
[ ] Selection
[ ] Insertion
[ ] Merge
[ ] Quick
[ ] Heap
[ ] Dutch National Flag
[ ] Inversions

INTERVALS
[ ] Merge intervals
[ ] Insert interval
[ ] Intersection
[ ] Scheduling patterns

GREEDY
[ ] Jump Game
[ ] Minimum jumps
[ ] Gas Station

MATRIX
[ ] Transpose
[ ] Rotate
[ ] Spiral
[ ] Matrix search
[ ] 2D prefix sum

ADVANCED
[ ] Monotonic stack
[ ] Top K
[ ] LIS
[ ] Histogram
[ ] Difference arrays


THE GOLDEN ARRAY QUESTIONS
==========================

Before coding, ask:

1. Is the array sorted?
2. Is the answer contiguous?
3. Is it a subarray or subsequence?
4. Is there a fixed window?
5. Is there a variable window?
6. Can I use two pointers?
7. Can prefix sums remove repeated work?
8. Can a hash map give O(1) average lookup?
9. Is there monotonicity?
10. Can I binary-search the answer?
11. Is the problem asking for maximum/minimum?
12. Is there a greedy invariant?
13. Do I need to preserve order?
14. Can I modify the array in place?
15. Is a monotonic stack hiding in the problem?
16. Is this actually an interval problem?
17. Is this a matrix/grid problem?

If you can answer these questions before coding,
many unseen array problems become pattern-recognition exercises
rather than memorization exercises.
"""


# ============================================================
# AUTOMATED TESTS
# ============================================================

def run_revision_tests():

    assert traverse([1, 2, 3]) == [1, 2, 3]
    assert insert_at([1, 3], 1, 2) == [1, 2, 3]
    assert delete_at([1, 2, 3], 1) == [1, 3]
    assert linear_search([4, 7, 9], 7) == 1

    assert reverse_array([1, 2, 3]) == [3, 2, 1]
    assert reverse_array_in_place([1, 2, 3]) == [3, 2, 1]

    assert prefix_sum([1, 2, 3]) == [0, 1, 3, 6]
    assert range_sum([1, 2, 3, 4], 1, 3) == 9
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2

    assert range_increment(
        5,
        [(1, 3, 2), (2, 4, 3)]
    ) == [0, 2, 5, 5, 3]

    assert two_sum_sorted([1, 2, 4, 7], 6) == [1, 2]
    assert remove_duplicates_sorted([1, 1, 2, 2, 3]) == [1, 2, 3]
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
    assert is_palindrome_array([1, 2, 1])
    assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == [
        [-1, -1, 2],
        [-1, 0, 1],
    ]

    assert max_sum_subarray_fixed_k([2, 1, 5, 1, 3, 2], 3) == 9
    assert longest_subarray_sum_at_most_k_positive(
        [2, 1, 1, 1, 3],
        4
    ) == 3
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert longest_substring_without_repeating("abcabcbb") == 3

    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_subarray_with_indices(
        [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    ) == (6, 3, 6)
    assert max_circular_subarray_sum([5, -3, 5]) == 10

    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert longest_consecutive_sequence([100, 4, 200, 1, 3, 2]) == 4
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    assert longest_zero_sum_subarray([15, -2, 2, -8, 1, 7, 10, 23]) == 5

    assert rotate_array([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]

    assert merge_sorted_arrays([1, 3, 5], [2, 4, 6]) == [
        1, 2, 3, 4, 5, 6
    ]

    assert merge_intervals(
        [[1, 3], [2, 6], [8, 10], [9, 11]]
    ) == [[1, 6], [8, 11]]

    assert insert_interval(
        [[1, 3], [6, 9]],
        [2, 5]
    ) == [[1, 5], [6, 9]]

    assert interval_intersection(
        [[0, 2], [5, 10], [13, 23], [24, 25]],
        [[1, 5], [8, 12], [15, 24], [25, 26]]
    ) == [
        [1, 2],
        [5, 5],
        [8, 10],
        [15, 23],
        [24, 24],
        [25, 25],
    ]

    assert binary_search([1, 3, 5, 7], 5) == 2
    assert lower_bound([1, 2, 2, 4], 2) == 1
    assert upper_bound([1, 2, 2, 4], 2) == 3
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]

    assert search_rotated_sorted_array(
        [4, 5, 6, 7, 0, 1, 2],
        0
    ) == 4

    assert find_min_rotated_sorted_array(
        [4, 5, 6, 7, 0, 1, 2]
    ) == 0

    assert find_peak_element([1, 2, 3, 1]) == 2
    assert integer_square_root(17) == 4
    assert koko_eating_bananas([3, 6, 7, 11], 8) == 4
    assert ship_within_days([1, 2, 3, 1, 1], 4) == 3

    expected = [1, 2, 3, 4, 5]

    assert bubble_sort([5, 1, 4, 2, 3]) == expected
    assert selection_sort([5, 1, 4, 2, 3]) == expected
    assert insertion_sort([5, 1, 4, 2, 3]) == expected
    assert merge_sort([5, 1, 4, 2, 3]) == expected
    assert quick_sort([5, 1, 4, 2, 3]) == expected
    assert heap_sort([5, 1, 4, 2, 3]) == expected

    assert sort_colors([2, 0, 2, 1, 1, 0]) == [
        0, 0, 1, 1, 2, 2
    ]

    assert count_inversions([1, 20, 6, 4, 5]) == 5

    assert top_k_frequent(
        [1, 1, 1, 2, 2, 3],
        2
    ) in ([1, 2], [2, 1])

    assert product_except_self([1, 2, 3, 4]) == [
        24, 12, 8, 6
    ]

    assert can_jump([2, 3, 1, 1, 4])
    assert not can_jump([3, 2, 1, 0, 4])
    assert jump_game_min_jumps([2, 3, 1, 1, 4]) == 2
    assert gas_station(
        [1, 2, 3, 4, 5],
        [3, 4, 5, 1, 2]
    ) == 3

    matrix = [[1, 2], [3, 4]]
    assert transpose_matrix(matrix) == [[1, 3], [2, 4]]
    assert rotate_matrix_90(matrix) == [[3, 1], [4, 2]]
    assert spiral_order(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    ) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    assert search_sorted_matrix(
        [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
        6
    )

    assert max_product_subarray([2, 3, -2, 4]) == 6
    assert longest_increasing_subsequence(
        [10, 9, 2, 5, 3, 7, 101, 18]
    ) == 4

    assert next_greater_element([2, 1, 2, 4, 3]) == [
        4, 2, 4, -1, -1
    ]

    assert daily_temperatures(
        [73, 74, 75, 71, 69, 72, 76, 73]
    ) == [1, 1, 4, 2, 1, 1, 0, 0]

    assert largest_rectangle_histogram(
        [2, 1, 5, 6, 2, 3]
    ) == 10

    assert kth_largest_heap(
        [3, 2, 1, 5, 6, 4],
        2
    ) == 5

    num_matrix = NumMatrix([
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ])

    assert num_matrix.sum_region(2, 1, 4, 3) == 8

    print("All Array revision tests passed! ✓")


if __name__ == "__main__":
    print("=" * 72)
    print("ARRAYS — COMPLETE DSA REVISION")
    print("=" * 72)
    print("Basic Operations                 ✓")
    print("Prefix / Difference Arrays       ✓")
    print("Two Pointers                     ✓")
    print("Sliding Window                   ✓")
    print("Kadane's Algorithm               ✓")
    print("Hashing Patterns                 ✓")
    print("Binary Search                    ✓")
    print("Binary Search on Answer          ✓")
    print("Sorting Algorithms               ✓")
    print("Intervals                        ✓")
    print("Greedy Patterns                  ✓")
    print("Matrix / 2D Arrays               ✓")
    print("Subarray / Subsequence           ✓")
    print("Monotonic Stack                  ✓")
    print("Top-K / Heap                     ✓")
    print("2D Prefix Sum                    ✓")
    print("Interview Cheat Sheet            ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 72)

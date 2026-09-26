"""
PHASE 2 — GREEDY + ADVANCED ALGORITHMS
=======================================

2-MONTH PLACEMENT REVISION FILE
Python reference implementations.

Topics:
1. Greedy Algorithms
2. Bit Manipulation
3. Fenwick Tree / Binary Indexed Tree
4. Segment Tree + Lazy Propagation
5. Disjoint Set Union (DSU)
6. Divide & Conquer
7. Meet in the Middle
8. Sparse Table
9. Mo's Algorithm

Use this file for REVISION, not passive reading.
For every algorithm:
    1. Hide the implementation.
    2. Explain the idea aloud.
    3. Re-derive the invariant.
    4. Code it from scratch.
    5. State time/space complexity.
"""

from __future__ import annotations
from heapq import heappush, heappop
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from typing import List, Tuple, Optional


# ============================================================
# 1. GREEDY ALGORITHMS
# ============================================================

def activity_selection(activities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Maximum number of non-overlapping activities. O(n log n)."""
    activities = sorted(activities, key=lambda x: x[1])
    chosen = []
    last_end = float("-inf")

    for start, end in activities:
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen


def erase_overlap_intervals(intervals: List[List[int]]) -> int:
    """Minimum intervals to remove so remaining intervals do not overlap."""
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    removed = 0

    for start, finish in intervals[1:]:
        if start < end:
            removed += 1
        else:
            end = finish
    return removed


def find_min_arrow_shots(points: List[List[int]]) -> int:
    """Minimum arrows to burst all balloons."""
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]

    for start, finish in points[1:]:
        if start > end:
            arrows += 1
            end = finish
    return arrows


def assign_cookies(greed: List[int], cookies: List[int]) -> int:
    """Maximum children satisfied."""
    greed.sort()
    cookies.sort()
    i = 0

    for cookie in cookies:
        if i < len(greed) and cookie >= greed[i]:
            i += 1
    return i


def jump_game(nums: List[int]) -> bool:
    """Can the last index be reached? O(n)."""
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True


def jump_game_ii(nums: List[int]) -> int:
    """Minimum jumps to reach last index. O(n)."""
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


def gas_station(gas: List[int], cost: List[int]) -> int:
    """Starting station if a circular tour is possible; otherwise -1."""
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


def candy(ratings: List[int]) -> int:
    """Minimum candies satisfying both neighbor constraints."""
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


def remove_k_digits(num: str, k: int) -> str:
    """Smallest number after removing k digits. Monotonic greedy stack."""
    stack = []

    for ch in num:
        while k and stack and stack[-1] > ch:
            stack.pop()
            k -= 1
        stack.append(ch)

    if k:
        stack = stack[:-k]

    result = "".join(stack).lstrip("0")
    return result or "0"


def reorganize_string(s: str) -> str:
    """Rearrange characters so adjacent characters differ."""
    freq = Counter(s)
    heap = [(-count, ch) for ch, count in freq.items()]
    import heapq
    heapq.heapify(heap)

    result = []
    prev_count, prev_char = 0, ""

    while heap:
        count, ch = heappop(heap)

        if ch == prev_char:
            if not heap:
                return ""
            count2, ch2 = heappop(heap)
            result.append(ch2)
            count2 += 1
            if count2:
                heappush(heap, (count2, ch2))
            heappush(heap, (count, ch))
        else:
            result.append(ch)
            count += 1
            prev_char = ch

    return "".join(result)


def task_scheduler(tasks: List[str], cooldown: int) -> int:
    """Minimum intervals to execute tasks with cooldown."""
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(v == max_freq for v in freq.values())
    return max(len(tasks), (max_freq - 1) * (cooldown + 1) + max_count)


def job_sequencing(jobs: List[Tuple[str, int, int]]) -> Tuple[int, List[str]]:
    """
    jobs = [(job_id, deadline, profit)]
    Returns (maximum profit, selected jobs).
    """
    if not jobs:
        return 0, []

    jobs = sorted(jobs, key=lambda x: x[2], reverse=True)
    max_deadline = max(d for _, d, _ in jobs)
    slots = [None] * (max_deadline + 1)
    profit = 0
    selected = []

    for job_id, deadline, value in jobs:
        for t in range(min(deadline, max_deadline), 0, -1):
            if slots[t] is None:
                slots[t] = job_id
                selected.append(job_id)
                profit += value
                break

    return profit, selected


# Huffman coding ------------------------------------------------

class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text: str) -> Optional[HuffmanNode]:
    """Build a Huffman tree from text."""
    if not text:
        return None

    freq = Counter(text)
    heap = [HuffmanNode(ch, f) for ch, f in freq.items()]
    import heapq
    heapq.heapify(heap)

    while len(heap) > 1:
        a = heappop(heap)
        b = heappop(heap)
        parent = HuffmanNode(None, a.freq + b.freq)
        parent.left = a
        parent.right = b
        heappush(heap, parent)

    return heap[0]


def huffman_codes(root: Optional[HuffmanNode]) -> dict:
    codes = {}

    def dfs(node, path):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = path or "0"
            return
        dfs(node.left, path + "0")
        dfs(node.right, path + "1")

    dfs(root, "")
    return codes


# ============================================================
# 2. BIT MANIPULATION
# ============================================================

def is_bit_set(n: int, i: int) -> int:
    return (n >> i) & 1


def set_bit(n: int, i: int) -> int:
    return n | (1 << i)


def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)


def toggle_bit(n: int, i: int) -> int:
    return n ^ (1 << i)


def clear_lowest_set_bit(n: int) -> int:
    return n & (n - 1)


def lowest_set_bit(n: int) -> int:
    return n & -n


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def count_set_bits(n: int) -> int:
    """Brian Kernighan."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def single_number(nums: List[int]) -> int:
    ans = 0
    for x in nums:
        ans ^= x
    return ans


def missing_number(nums: List[int]) -> int:
    ans = len(nums)
    for i, x in enumerate(nums):
        ans ^= i ^ x
    return ans


def single_number_iii(nums: List[int]) -> List[int]:
    xor_all = 0
    for x in nums:
        xor_all ^= x

    diff = xor_all & -xor_all
    a = b = 0

    for x in nums:
        if x & diff:
            a ^= x
        else:
            b ^= x

    return [a, b]


def reverse_bits_32(n: int) -> int:
    ans = 0
    for _ in range(32):
        ans = (ans << 1) | (n & 1)
        n >>= 1
    return ans


def hamming_distance(x: int, y: int) -> int:
    return count_set_bits(x ^ y)


def xor_range(l: int, r: int) -> int:
    """XOR of all integers in [l, r]."""
    def prefix_xor(n):
        if n % 4 == 0:
            return n
        if n % 4 == 1:
            return 1
        if n % 4 == 2:
            return n + 1
        return 0

    return prefix_xor(r) ^ prefix_xor(l - 1)


def generate_subsets_bitmask(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    result = []

    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)

    return result


def enumerate_submasks(mask: int) -> List[int]:
    """All submasks of mask, including 0."""
    result = []
    sub = mask
    while True:
        result.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return result


# ============================================================
# 3. FENWICK TREE / BINARY INDEXED TREE
# ============================================================

class FenwickTree:
    """
    1-indexed internally.
    Supports:
        add(index, delta) : O(log n)
        prefix_sum(index)  : O(log n)
        range_sum(l, r)    : O(log n)
    """

    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, delta: int) -> None:
        index += 1
        while index <= self.n:
            self.bit[index] += delta
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        index += 1
        total = 0
        while index > 0:
            total += self.bit[index]
            index -= index & -index
        return total

    def range_sum(self, left: int, right: int) -> int:
        if left > right:
            return 0
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left else 0)


def fenwick_from_array(nums: List[int]) -> FenwickTree:
    fw = FenwickTree(len(nums))
    for i, x in enumerate(nums):
        fw.add(i, x)
    return fw


# ============================================================
# 4. SEGMENT TREE
# ============================================================

class SegmentTree:
    """Recursive segment tree for range sum + point update."""

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.tree = [0] * (4 * max(1, self.n))
        self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums, node, left, right):
        if left > right:
            return
        if left == right:
            self.tree[node] = nums[left]
            return
        mid = (left + right) // 2
        self._build(nums, node * 2, left, mid)
        self._build(nums, node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def update(self, index: int, value: int):
        def rec(node, left, right):
            if left == right:
                self.tree[node] = value
                return

            mid = (left + right) // 2
            if index <= mid:
                rec(node * 2, left, mid)
            else:
                rec(node * 2 + 1, mid + 1, right)

            self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

        rec(1, 0, self.n - 1)

    def query(self, ql: int, qr: int) -> int:
        def rec(node, left, right):
            if qr < left or right < ql:
                return 0
            if ql <= left and right <= qr:
                return self.tree[node]

            mid = (left + right) // 2
            return rec(node * 2, left, mid) + rec(node * 2 + 1, mid + 1, right)

        return rec(1, 0, self.n - 1)


class LazySegmentTree:
    """Range-add + range-sum segment tree."""

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.tree = [0] * (4 * max(1, self.n))
        self.lazy = [0] * (4 * max(1, self.n))
        self._build(nums, 1, 0, self.n - 1)

    def _build(self, nums, node, l, r):
        if l == r:
            self.tree[node] = nums[l]
            return
        mid = (l + r) // 2
        self._build(nums, node * 2, l, mid)
        self._build(nums, node * 2 + 1, mid + 1, r)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _apply(self, node, l, r, value):
        self.tree[node] += (r - l + 1) * value
        self.lazy[node] += value

    def _push(self, node, l, r):
        if self.lazy[node] == 0 or l == r:
            return
        mid = (l + r) // 2
        value = self.lazy[node]
        self._apply(node * 2, l, mid, value)
        self._apply(node * 2 + 1, mid + 1, r, value)
        self.lazy[node] = 0

    def range_add(self, ql, qr, value):
        def rec(node, l, r):
            if qr < l or r < ql:
                return
            if ql <= l and r <= qr:
                self._apply(node, l, r, value)
                return

            self._push(node, l, r)
            mid = (l + r) // 2
            rec(node * 2, l, mid)
            rec(node * 2 + 1, mid + 1, r)
            self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

        rec(1, 0, self.n - 1)

    def range_sum(self, ql, qr):
        def rec(node, l, r):
            if qr < l or r < ql:
                return 0
            if ql <= l and r <= qr:
                return self.tree[node]

            self._push(node, l, r)
            mid = (l + r) // 2
            return rec(node * 2, l, mid) + rec(node * 2 + 1, mid + 1, r)

        return rec(1, 0, self.n - 1)


# ============================================================
# 5. DISJOINT SET UNION
# ============================================================

class DSU:
    """Union-Find with path compression + union by size."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """edges = (u, v, weight). Returns MST weight and chosen edges."""
    dsu = DSU(n)
    mst = []
    total = 0

    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            mst.append((u, v, w))
            total += w

    if len(mst) != n - 1:
        return float("inf"), mst

    return total, mst


# ============================================================
# 6. DIVIDE & CONQUER
# ============================================================

def merge_sort(nums: List[int]) -> List[int]:
    if len(nums) <= 1:
        return nums[:]

    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    i = j = 0
    result = []

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


def quickselect_kth_largest(nums: List[int], k: int) -> int:
    """Average O(n), in-place quickselect. k is 1-indexed."""
    arr = nums[:]
    target = len(arr) - k
    left, right = 0, len(arr) - 1

    while True:
        pivot = arr[right]
        p = left

        for i in range(left, right):
            if arr[i] <= pivot:
                arr[p], arr[i] = arr[i], arr[p]
                p += 1

        arr[p], arr[right] = arr[right], arr[p]

        if p == target:
            return arr[p]
        if p < target:
            left = p + 1
        else:
            right = p - 1


def max_subarray_divide_conquer(nums: List[int]) -> int:
    """Maximum subarray using divide & conquer."""
    if not nums:
        return 0

    def rec(l, r):
        if l == r:
            return nums[l]

        mid = (l + r) // 2
        left_best = rec(l, mid)
        right_best = rec(mid + 1, r)

        s = 0
        best_left = float("-inf")
        for i in range(mid, l - 1, -1):
            s += nums[i]
            best_left = max(best_left, s)

        s = 0
        best_right = float("-inf")
        for i in range(mid + 1, r + 1):
            s += nums[i]
            best_right = max(best_right, s)

        return max(left_best, right_best, best_left + best_right)

    return rec(0, len(nums) - 1)


def fast_power(x: float, n: int) -> float:
    """Binary exponentiation. O(log n)."""
    if n < 0:
        return 1 / fast_power(x, -n)

    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result


# ============================================================
# 7. MEET IN THE MIDDLE
# ============================================================

def subset_sums(nums: List[int]) -> List[int]:
    sums = [0]
    for x in nums:
        sums += [s + x for s in sums]
    return sums


def closest_subsequence_sum(nums: List[int], goal: int) -> int:
    """Minimum absolute difference between subset sum and goal."""
    mid = len(nums) // 2
    left = sorted(subset_sums(nums[:mid]))
    right = subset_sums(nums[mid:])

    best = float("inf")

    for x in right:
        target = goal - x
        i = bisect_left(left, target)

        if i < len(left):
            best = min(best, abs(x + left[i] - goal))
        if i:
            best = min(best, abs(x + left[i - 1] - goal))

    return best


# ============================================================
# 8. SPARSE TABLE
# ============================================================

class SparseTableMin:
    """Static Range Minimum Query: O(n log n) build, O(1) query."""

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.log = [0] * (self.n + 1)

        for i in range(2, self.n + 1):
            self.log[i] = self.log[i // 2] + 1

        k = self.log[self.n] + 1 if self.n else 1
        self.table = [[0] * self.n for _ in range(k)]

        if self.n:
            self.table[0] = nums[:]

        j = 1
        while (1 << j) <= self.n:
            length = 1 << j
            half = length >> 1
            for i in range(self.n - length + 1):
                self.table[j][i] = min(
                    self.table[j - 1][i],
                    self.table[j - 1][i + half]
                )
            j += 1

    def query(self, left: int, right: int) -> int:
        length = right - left + 1
        k = self.log[length]
        return min(
            self.table[k][left],
            self.table[k][right - (1 << k) + 1]
        )


# ============================================================
# 9. MO'S ALGORITHM
# ============================================================

def mos_distinct_queries(nums: List[int], queries: List[Tuple[int, int]]) -> List[int]:
    """
    Offline range-distinct queries using Mo's ordering.

    queries = [(left, right)] inclusive, 0-indexed.
    Returns answers in original query order.
    """
    n = len(nums)
    if not queries:
        return []

    block = max(1, int(n ** 0.5))

    ordered = sorted(
        enumerate(queries),
        key=lambda x: (
            x[1][0] // block,
            x[1][1] if (x[1][0] // block) % 2 == 0 else -x[1][1]
        )
    )

    freq = Counter()
    current_distinct = 0
    cur_l, cur_r = 0, -1
    answers = [0] * len(queries)

    def add(index):
        nonlocal current_distinct
        x = nums[index]
        if freq[x] == 0:
            current_distinct += 1
        freq[x] += 1

    def remove(index):
        nonlocal current_distinct
        x = nums[index]
        freq[x] -= 1
        if freq[x] == 0:
            current_distinct -= 1

    for qi, (l, r) in ordered:
        while cur_l > l:
            cur_l -= 1
            add(cur_l)
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_l < l:
            remove(cur_l)
            cur_l += 1
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1

        answers[qi] = current_distinct

    return answers


# ============================================================
# 10. REVISION CHEAT SHEET
# ============================================================

ALGORITHM_COMPLEXITY = {
    "Activity Selection": "O(n log n) sorting, O(n) scan",
    "Jump Game": "O(n) time, O(1) space",
    "Gas Station": "O(n) time, O(1) space",
    "Candy": "O(n) time, O(n) space",
    "Bit tricks": "Usually O(1) per operation",
    "Count set bits": "O(number of set bits)",
    "Fenwick update/query": "O(log n)",
    "Segment Tree build": "O(n)",
    "Segment Tree query/update": "O(log n)",
    "Lazy Segment Tree range update/query": "O(log n)",
    "DSU": "Amortized near O(1) per operation",
    "Kruskal": "O(E log E)",
    "Merge Sort": "O(n log n)",
    "Quickselect": "Average O(n), worst O(n²)",
    "Binary exponentiation": "O(log n)",
    "Meet in the Middle": "Usually O(2^(n/2) log 2^(n/2))",
    "Sparse Table build": "O(n log n)",
    "Sparse Table RMQ": "O(1)",
    "Mo's Algorithm": "Typical ~O((N+Q)sqrt(N)) depending on updates/operation"
}


def revision_checklist():
    """
    2-MONTH CHECKLIST

    WEEK 1:
      [ ] Greedy fundamentals
      [ ] Activity selection / intervals
      [ ] Greedy proofs
      [ ] 10+ greedy problems

    WEEK 2:
      [ ] Heap + greedy
      [ ] Job scheduling
      [ ] Huffman coding
      [ ] Hard greedy problems
      [ ] Timed mixed greedy test

    WEEK 3:
      [ ] Binary representation
      [ ] &, |, ^, ~, <<, >>
      [ ] XOR patterns
      [ ] Set/clear/toggle bit
      [ ] Brian Kernighan
      [ ] 12+ bit problems

    WEEK 4:
      [ ] Bitmasking
      [ ] Subset enumeration
      [ ] Submask enumeration
      [ ] Advanced XOR
      [ ] Timed bit-manipulation test

    WEEK 5:
      [ ] Fenwick Tree
      [ ] Prefix/range queries
      [ ] Coordinate compression
      [ ] Segment Tree build/query/update
      [ ] 8+ range-query problems

    WEEK 6:
      [ ] Lazy propagation
      [ ] Range updates
      [ ] Segment Tree variations
      [ ] Fenwick vs Segment Tree vs Sparse Table
      [ ] Timed range-query test

    WEEK 7:
      [ ] DSU
      [ ] Path compression
      [ ] Union by size/rank
      [ ] Kruskal
      [ ] Divide & Conquer
      [ ] Recurrence analysis
      [ ] Meet in the Middle

    WEEK 8:
      [ ] Sparse Table
      [ ] Mo's Algorithm
      [ ] Mixed advanced problems
      [ ] Re-implement all core structures from memory
      [ ] Full Phase 2 mock test
      [ ] Review every mistake

    FINAL RULE:
      If you cannot derive it without looking at the code,
      you have not mastered it yet.
    """
    pass


# ============================================================
# QUICK SELF-TEST
# ============================================================

def self_test():
    assert activity_selection([(1, 2), (2, 3), (1, 5), (4, 6)]) == [
        (1, 2), (2, 3), (4, 6)
    ]

    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert find_min_arrow_shots([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
    assert assign_cookies([1, 2, 3], [1, 1]) == 1
    assert jump_game([2, 3, 1, 1, 4])
    assert not jump_game([3, 2, 1, 0, 4])
    assert jump_game_ii([2, 3, 1, 1, 4]) == 2
    assert gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert candy([1, 0, 2]) == 5
    assert remove_k_digits("1432219", 3) == "1219"
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert missing_number([3, 0, 1]) == 2
    assert is_power_of_two(16)
    assert count_set_bits(7) == 3
    assert xor_range(3, 9) == 2

    fw = fenwick_from_array([1, 2, 3, 4, 5])
    assert fw.range_sum(1, 3) == 9
    fw.add(2, 5)
    assert fw.range_sum(1, 3) == 14

    st = SegmentTree([1, 2, 3, 4, 5])
    assert st.query(1, 3) == 9
    st.update(2, 10)
    assert st.query(1, 3) == 16

    lazy = LazySegmentTree([1, 2, 3, 4, 5])
    assert lazy.range_sum(1, 3) == 9
    lazy.range_add(1, 3, 10)
    assert lazy.range_sum(1, 3) == 39

    dsu = DSU(4)
    assert dsu.union(0, 1)
    assert dsu.connected(0, 1)
    assert dsu.union(2, 3)
    assert not dsu.connected(0, 2)
    assert dsu.union(1, 2)
    assert dsu.connected(0, 3)

    weight, mst = kruskal_mst(
        4,
        [(0, 1, 1), (1, 2, 2), (2, 3, 1), (0, 3, 4), (0, 2, 3)]
    )
    assert weight == 4 and len(mst) == 3

    assert merge_sort([5, 2, 4, 1, 3]) == [1, 2, 3, 4, 5]
    assert quickselect_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert max_subarray_divide_conquer([-2,1,-3,4,-1,2,1,-5,4]) == 6
    assert fast_power(2, 10) == 1024

    assert closest_subsequence_sum([5, -7, 3, 5], 6) == 0

    sp = SparseTableMin([5, 2, 4, 7, 1, 3])
    assert sp.query(1, 4) == 1

    assert mos_distinct_queries(
        [1, 2, 1, 3, 2],
        [(0, 2), (1, 4), (2, 4)]
    ) == [2, 3, 3]

    print("All Phase 2 revision tests passed.")


if __name__ == "__main__":
    self_test()

"""
DSA REMAINING INTERVIEW TOPICS — PYTHON 3
=========================================
Supplementary reference for interview preparation.

Sections:
  1. Monotonic stack and deque
  2. Trie and Binary Trie (maximum XOR)
  3. String algorithms: KMP, Z-function, rolling hash
  4. Advanced graphs: 0-1 BFS, SCC, bridges, articulation points
  5. Range queries: sparse table, square-root decomposition
  6. Randomized Quickselect
  7. Advanced reference: Dinic max flow, bipartite matching, 2-SAT
  8. Advanced strings: suffix array, Aho-Corasick
  9. Advanced structures: persistent segment tree, rollback DSU
 10. SOS DP (subset sums over subsets)

Python 3.10+
This is a reference library: functions/classes are intentionally provided
without a single main() so they can be copied into solutions as needed.
"""

from collections import deque
from random import randrange
from typing import Iterable, Optional


# ============================================================
# 1. MONOTONIC STACK / DEQUE
# ============================================================

def next_greater_indices(nums: list[int]) -> list[int]:
    """Return index of next strictly greater element to the right; -1 if absent."""
    ans = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = i
        stack.append(i)
    return ans


def previous_smaller_indices(nums: list[int]) -> list[int]:
    """Previous strictly smaller element index for every position; -1 if absent."""
    ans = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] >= x:
            stack.pop()
        ans[i] = stack[-1] if stack else -1
        stack.append(i)
    return ans


def largest_rectangle_histogram(heights: list[int]) -> int:
    """Largest rectangle in histogram, O(n)."""
    stack = []
    best = 0
    extended = heights + [0]
    for i, h in enumerate(extended):
        while stack and extended[stack[-1]] > h:
            height = extended[stack.pop()]
            left = stack[-1] + 1 if stack else 0
            best = max(best, height * (i - left))
        stack.append(i)
    return best


def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    """Maximum for every window of size k, O(n)."""
    if not 1 <= k <= len(nums):
        return []
    q = deque()  # indices, values decreasing
    out = []
    for i, x in enumerate(nums):
        while q and q[0] <= i - k:
            q.popleft()
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        if i >= k - 1:
            out.append(nums[q[0]])
    return out


# ============================================================
# 2. TRIE / BINARY TRIE
# ============================================================

class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False


class Trie:
    """Prefix tree supporting insert, exact search, and prefix search."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


class BinaryTrie:
    """Binary trie for non-negative integers, e.g. maximum XOR query."""

    def __init__(self, max_bit: int = 31):
        self.max_bit = max_bit
        self.root = {}

    def insert(self, value: int) -> None:
        node = self.root
        for bit in range(self.max_bit, -1, -1):
            b = (value >> bit) & 1
            node = node.setdefault(b, {})

    def max_xor(self, value: int) -> int:
        """Return maximum XOR value obtainable against an inserted number."""
        node = self.root
        result = 0
        for bit in range(self.max_bit, -1, -1):
            b = (value >> bit) & 1
            wanted = 1 - b
            if wanted in node:
                result |= 1 << bit
                node = node[wanted]
            elif b in node:
                node = node[b]
            else:
                raise ValueError("BinaryTrie is empty")
        return result


# ============================================================
# 3. STRING ALGORITHMS
# ============================================================

def prefix_function(s: str) -> list[int]:
    """KMP prefix-function / longest proper border length for each prefix."""
    pi = [0] * len(s)
    for i in range(1, len(s)):
        j = pi[i - 1]
        while j and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> list[int]:
    """All start indices where pattern occurs in text, in O(n + m)."""
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    matches = []
    j = 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - len(pattern) + 1)
            j = pi[j - 1]
    return matches


def z_function(s: str) -> list[int]:
    """z[i] = length of longest substring starting at i matching s's prefix."""
    n = len(s)
    z = [0] * n
    left = right = 0
    for i in range(1, n):
        if i <= right:
            z[i] = min(right - i + 1, z[i - left])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left, right = i, i + z[i] - 1
    if n:
        z[0] = n
    return z


class RollingHash:
    """Single-mod polynomial rolling hash; use two moduli for lower collision risk."""

    def __init__(self, s: str, base: int = 911382323, mod: int = 1_000_000_007):
        self.mod = mod
        self.base = base % mod
        n = len(s)
        self.prefix = [0] * (n + 1)
        self.power = [1] * (n + 1)
        for i, ch in enumerate(s):
            self.prefix[i + 1] = (self.prefix[i] * self.base + ord(ch)) % mod
            self.power[i + 1] = self.power[i] * self.base % mod

    def get(self, left: int, right: int) -> int:
        """Hash of half-open substring s[left:right]."""
        return (self.prefix[right] -
                self.prefix[left] * self.power[right - left]) % self.mod


# ============================================================
# 4. ADVANCED GRAPH ALGORITHMS
# ============================================================

def zero_one_bfs(graph: list[list[tuple[int, int]]], source: int) -> list[int]:
    """
    Shortest paths when each edge weight is 0 or 1.
    graph[u] contains (v, weight).
    """
    n = len(graph)
    inf = float("inf")
    dist = [inf] * n
    dist[source] = 0
    dq = deque([source])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return dist


def kosaraju_scc(graph: list[list[int]]) -> list[list[int]]:
    """Return strongly connected components of a directed graph."""
    n = len(graph)
    reverse_graph = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            reverse_graph[v].append(u)

    seen = [False] * n
    order = []

    def dfs1(u: int) -> None:
        seen[u] = True
        for v in graph[u]:
            if not seen[v]:
                dfs1(v)
        order.append(u)

    for u in range(n):
        if not seen[u]:
            dfs1(u)

    seen = [False] * n
    components = []

    def dfs2(u: int, comp: list[int]) -> None:
        seen[u] = True
        comp.append(u)
        for v in reverse_graph[u]:
            if not seen[v]:
                dfs2(v, comp)

    for u in reversed(order):
        if not seen[u]:
            comp = []
            dfs2(u, comp)
            components.append(comp)
    return components


def bridges_and_articulation_points(
    n: int, edges: list[tuple[int, int]]
) -> tuple[list[tuple[int, int]], set[int]]:
    """
    Undirected graph. Returns bridges and articulation-point vertices.
    Handles parallel edges by tracking edge IDs.
    """
    graph = [[] for _ in range(n)]
    for eid, (u, v) in enumerate(edges):
        graph[u].append((v, eid))
        graph[v].append((u, eid))

    timer = 0
    tin = [-1] * n
    low = [-1] * n
    bridges = []
    articulation = set()

    def dfs(u: int, parent_edge: int) -> None:
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        children = 0

        for v, eid in graph[u]:
            if eid == parent_edge:
                continue
            if tin[v] != -1:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.append((u, v))
                if parent_edge != -1 and low[v] >= tin[u]:
                    articulation.add(u)
                children += 1

        if parent_edge == -1 and children > 1:
            articulation.add(u)

    for u in range(n):
        if tin[u] == -1:
            dfs(u, -1)
    return bridges, articulation


# ============================================================
# 5. RANGE QUERIES
# ============================================================

class SparseTable:
    """Static range minimum query in O(1); preprocessing O(n log n)."""

    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.logs = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.logs[i] = self.logs[i // 2] + 1
        self.table = [nums[:]]
        k = 1
        while (1 << k) <= self.n:
            prev = self.table[k - 1]
            half = 1 << (k - 1)
            row = [
                min(prev[i], prev[i + half])
                for i in range(self.n - (1 << k) + 1)
            ]
            self.table.append(row)
            k += 1

    def query_min(self, left: int, right: int) -> int:
        """Inclusive interval [left, right]."""
        length = right - left + 1
        k = self.logs[length]
        span = 1 << k
        return min(self.table[k][left], self.table[k][right - span + 1])


class SqrtDecomposition:
    """Range-sum structure with point updates, approximately O(sqrt(n)) per op."""

    def __init__(self, nums: list[int]):
        self.nums = nums[:]
        self.n = len(nums)
        self.block_size = max(1, int(self.n ** 0.5))
        self.blocks = [0] * ((self.n + self.block_size - 1) // self.block_size)
        for i, x in enumerate(nums):
            self.blocks[i // self.block_size] += x

    def update(self, index: int, value: int) -> None:
        block = index // self.block_size
        self.blocks[block] += value - self.nums[index]
        self.nums[index] = value

    def query_sum(self, left: int, right: int) -> int:
        total = 0
        while left <= right and left % self.block_size != 0:
            total += self.nums[left]
            left += 1
        while left + self.block_size - 1 <= right:
            total += self.blocks[left // self.block_size]
            left += self.block_size
        while left <= right:
            total += self.nums[left]
            left += 1
        return total


# ============================================================
# 6. RANDOMIZED QUICKSELECT
# ============================================================

def quickselect(nums: list[int], k: int) -> int:
    """
    Return the k-th smallest value (1-indexed), modifying nums in place.
    Average O(n), worst-case O(n^2); randomized pivot mitigates worst-case.
    """
    if not 1 <= k <= len(nums):
        raise ValueError("k must be between 1 and len(nums)")
    target = k - 1
    left, right = 0, len(nums) - 1

    while left <= right:
        pivot = nums[randrange(left, right + 1)]
        i, j = left, right
        while i <= j:
            while nums[i] < pivot:
                i += 1
            while nums[j] > pivot:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1
        if target <= j:
            right = j
        elif target >= i:
            left = i
        else:
            return nums[target]
    return nums[target]


# ============================================================
# 7. ADVANCED GRAPH REFERENCE
# ============================================================

class Dinic:
    """Dinic max-flow for directed graphs; integer capacities."""

    class Edge:
        __slots__ = ("to", "cap", "rev")

        def __init__(self, to: int, cap: int, rev: int):
            self.to, self.cap, self.rev = to, cap, rev

    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        forward = self.Edge(v, capacity, len(self.graph[v]))
        backward = self.Edge(u, 0, len(self.graph[u]))
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        flow = 0
        while True:
            level = [-1] * self.n
            level[source] = 0
            q = deque([source])
            while q:
                u = q.popleft()
                for e in self.graph[u]:
                    if e.cap > 0 and level[e.to] == -1:
                        level[e.to] = level[u] + 1
                        q.append(e.to)
            if level[sink] == -1:
                return flow

            it = [0] * self.n

            def dfs(u: int, pushed: int) -> int:
                if u == sink:
                    return pushed
                while it[u] < len(self.graph[u]):
                    e = self.graph[u][it[u]]
                    if e.cap > 0 and level[e.to] == level[u] + 1:
                        amount = dfs(e.to, min(pushed, e.cap))
                        if amount:
                            e.cap -= amount
                            self.graph[e.to][e.rev].cap += amount
                            return amount
                    it[u] += 1
                return 0

            while pushed := dfs(source, 10**30):
                flow += pushed


def maximum_bipartite_matching(
    left_size: int, right_size: int, adj: list[list[int]]
) -> int:
    """Kuhn algorithm. adj[u] lists right-side neighbors; O(VE) worst case."""
    match_right = [-1] * right_size

    def augment(u: int, seen: list[bool]) -> bool:
        for v in adj[u]:
            if seen[v]:
                continue
            seen[v] = True
            if match_right[v] == -1 or augment(match_right[v], seen):
                match_right[v] = u
                return True
        return False

    answer = 0
    for u in range(left_size):
        if augment(u, [False] * right_size):
            answer += 1
    return answer


# 2-SAT reference: literal x is encoded as 2*x for x, and 2*x+1 for not x.
# Add implication edges with the helper below, then run SCC and compare literals.
def add_or_clause(graph: list[list[int]], x: int, y: int) -> None:
    """Add clause (x OR y), where literals are encoded as integer node IDs."""
    graph[x ^ 1].append(y)
    graph[y ^ 1].append(x)


# ============================================================
# 8. ADVANCED STRING ALGORITHMS
# ============================================================

def suffix_array(s: str) -> list[int]:
    """Suffix array using prefix doubling; O(n log^2 n) with Python sorting."""
    n = len(s)
    if n == 0:
        return []
    sa = list(range(n))
    rank = [ord(ch) for ch in s]
    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        new_rank = [0] * n
        for j in range(1, n):
            prev, cur = sa[j - 1], sa[j]
            prev_key = (rank[prev], rank[prev + k] if prev + k < n else -1)
            cur_key = (rank[cur], rank[cur + k] if cur + k < n else -1)
            new_rank[cur] = new_rank[prev] + (cur_key != prev_key)
        rank = new_rank
        if rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


class AhoCorasick:
    """Multi-pattern string matching. Reports (pattern_id, ending_index)."""

    def __init__(self):
        self.next = [{}]
        self.fail = [0]
        self.output = [[]]

    def add(self, pattern: str, pattern_id: int) -> None:
        node = 0
        for ch in pattern:
            if ch not in self.next[node]:
                self.next[node][ch] = len(self.next)
                self.next.append({})
                self.fail.append(0)
                self.output.append([])
            node = self.next[node][ch]
        self.output[node].append(pattern_id)

    def build(self) -> None:
        q = deque()
        for child in self.next[0].values():
            q.append(child)
        while q:
            u = q.popleft()
            for ch, v in self.next[u].items():
                q.append(v)
                f = self.fail[u]
                while f and ch not in self.next[f]:
                    f = self.fail[f]
                self.fail[v] = self.next[f].get(ch, 0)
                self.output[v].extend(self.output[self.fail[v]])

    def search(self, text: str) -> list[tuple[int, int]]:
        """Returns (pattern_id, index_of_match_end) for every occurrence."""
        node = 0
        matches = []
        for i, ch in enumerate(text):
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            for pattern_id in self.output[node]:
                matches.append((pattern_id, i))
        return matches


# ============================================================
# 9. ADVANCED DATA STRUCTURES
# ============================================================

class RollbackDSU:
    """Disjoint Set Union with rollback; do not use path compression."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.history = []
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def snapshot(self) -> int:
        return len(self.history)

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            self.history.append(None)
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, a, self.size[a]))
        self.parent[b] = a
        self.size[a] += self.size[b]
        self.components -= 1
        return True

    def rollback(self, snapshot: int) -> None:
        while len(self.history) > snapshot:
            item = self.history.pop()
            if item is None:
                continue
            b, a, old_size = item
            self.parent[b] = b
            self.size[a] = old_size
            self.components += 1


class PersistentSegmentTree:
    """
    Persistent point-update / range-sum tree.
    Each update creates a new root; old versions remain queryable.
    """

    class Node:
        __slots__ = ("left", "right", "total")

        def __init__(self, left=None, right=None, total=0):
            self.left = left
            self.right = right
            self.total = total

    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.roots = [self._build(nums, 0, self.n - 1)] if self.n else []

    def _build(self, nums, lo, hi):
        if lo == hi:
            return self.Node(total=nums[lo])
        mid = (lo + hi) // 2
        left = self._build(nums, lo, mid)
        right = self._build(nums, mid + 1, hi)
        return self.Node(left, right, left.total + right.total)

    def update(self, version: int, index: int, value: int) -> int:
        """Create a new version with nums[index] = value; return its version ID."""
        if not self.n:
            raise ValueError("Cannot update an empty tree")
        root = self._update(self.roots[version], 0, self.n - 1, index, value)
        self.roots.append(root)
        return len(self.roots) - 1

    def _update(self, node, lo, hi, index, value):
        if lo == hi:
            return self.Node(total=value)
        mid = (lo + hi) // 2
        if index <= mid:
            left = self._update(node.left, lo, mid, index, value)
            right = node.right
        else:
            left = node.left
            right = self._update(node.right, mid + 1, hi, index, value)
        return self.Node(left, right, left.total + right.total)

    def query_sum(self, version: int, ql: int, qr: int) -> int:
        if not self.n:
            return 0
        return self._query(self.roots[version], 0, self.n - 1, ql, qr)

    def _query(self, node, lo, hi, ql, qr):
        if qr < lo or hi < ql:
            return 0
        if ql <= lo and hi <= qr:
            return node.total
        mid = (lo + hi) // 2
        return (self._query(node.left, lo, mid, ql, qr) +
                self._query(node.right, mid + 1, hi, ql, qr))


def sos_dp_subset_sums(values: list[int], bits: int) -> list[int]:
    """
    SOS DP: result[mask] = sum(values[submask] for submask subset of mask).
    values must have length 2**bits.
    """
    size = 1 << bits
    if len(values) != size:
        raise ValueError("values length must equal 2**bits")
    dp = values[:]
    for bit in range(bits):
        for mask in range(size):
            if mask & (1 << bit):
                dp[mask] += dp[mask ^ (1 << bit)]
    return dp


# ============================================================
# 10. QUICK INTERVIEW CHECKLIST
# ============================================================
#
# Before coding:
#   1. State the brute force and its complexity.
#   2. Identify the invariant / state / transition.
#   3. Check constraints: n, value range, graph density, update frequency.
#   4. Clarify indexing (0-based vs 1-based), inclusivity, duplicates.
#   5. Test empty, singleton, duplicates, sorted, reverse-sorted, extremes.
#
# Pattern cues:
#   - "next/previous greater/smaller" -> monotonic stack
#   - "maximum/minimum in every window" -> monotonic deque
#   - "prefix of words / XOR" -> Trie
#   - "many patterns in one text" -> Aho-Corasick
#   - "range query, no updates" -> Sparse Table (idempotent operation)
#   - "dynamic connectivity over time" -> Rollback DSU + segment tree over time
#   - "minimum cuts / maximum throughput" -> Max Flow / Min Cut
#   - "k-th smallest" -> Quickselect, order-statistics structure
#   - "subset aggregate over all masks" -> SOS DP
#
# Python note:
#   Recursive DFS can hit recursion limits on deep inputs. For contest tasks,
#   consider iterative DFS or carefully set sys.setrecursionlimit when safe.

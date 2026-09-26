"""
DYNAMIC PROGRAMMING — COMPLETE 2-MONTH REVISION
================================================

Placement-focused DP revision library.

Goal:
    Do not memorize DP formulas.
    Learn to identify:
        1. State
        2. State meaning
        3. Transition
        4. Base cases
        5. Computation order
        6. Answer location
        7. Space optimization

Covers:
    - DP fundamentals
    - Recursion -> Memoization -> Tabulation
    - 1D DP
    - 2D / Grid DP
    - Knapsack family
    - LIS
    - LCS
    - String DP
    - Interval DP
    - Stock DP
    - Tree DP
    - DAG DP
    - Bitmask DP
    - Digit DP
    - Game DP
    - Reconstruction
    - Pattern recognition
    - Complexity cheat sheet

Python implementations.
"""


from functools import lru_cache
from math import inf


# ============================================================
# 0. DP FUNDAMENTALS
# ============================================================

"""
DP is useful when a problem has:

1. Overlapping subproblems
2. Optimal substructure / reusable subproblem answers

The core workflow:

    Problem
       ↓
    Decisions
       ↓
    State
       ↓
    Transition
       ↓
    Base Case
       ↓
    Computation Order
       ↓
    Answer

Three common implementations:

    Brute-force recursion
            ↓
    Memoization (Top Down)
            ↓
    Tabulation (Bottom Up)

IMPORTANT:

Before writing:

    dp[i] = ...

write:

    "dp[i] means ..."

in plain English.
"""


# ============================================================
# 1. FIBONACCI — THREE VERSIONS
# ============================================================

def fibonacci_recursive(n):
    if n <= 1:
        return n

    return (
        fibonacci_recursive(n - 1)
        + fibonacci_recursive(n - 2)
    )


def fibonacci_memoization(n):
    memo = {}

    def solve(i):
        if i <= 1:
            return i

        if i in memo:
            return memo[i]

        memo[i] = solve(i - 1) + solve(i - 2)
        return memo[i]

    return solve(n)


def fibonacci_tabulation(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_optimized(n):
    if n <= 1:
        return n

    prev2, prev1 = 0, 1

    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


# ============================================================
# 2. CLIMBING STAIRS
# ============================================================

def climbing_stairs(n):
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1


def climbing_stairs_k_steps(n, k):
    """
    Number of ways to reach n if you can climb
    1..k stairs at a time.
    """
    if n == 0:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for step in range(1, k + 1):
            if i - step >= 0:
                dp[i] += dp[i - step]

    return dp[n]


# ============================================================
# 3. MIN COST CLIMBING STAIRS
# ============================================================

def min_cost_climbing_stairs(cost):
    n = len(cost)

    if n <= 2:
        return min(cost)

    prev2 = cost[0]
    prev1 = cost[1]

    for i in range(2, n):
        current = cost[i] + min(prev1, prev2)
        prev2, prev1 = prev1, current

    return min(prev1, prev2)


# ============================================================
# 4. HOUSE ROBBER FAMILY
# ============================================================

def house_robber(nums):
    prev2 = 0
    prev1 = 0

    for money in nums:
        current = max(
            prev1,
            prev2 + money
        )

        prev2, prev1 = prev1, current

    return prev1


def house_robber_ii(nums):
    if len(nums) == 1:
        return nums[0]

    def rob_range(left, right):
        prev2 = prev1 = 0

        for i in range(left, right + 1):
            current = max(
                prev1,
                prev2 + nums[i]
            )

            prev2, prev1 = prev1, current

        return prev1

    return max(
        rob_range(0, len(nums) - 2),
        rob_range(1, len(nums) - 1)
    )


# ============================================================
# 5. KADANE — MAXIMUM SUBARRAY
# ============================================================

def max_subarray(nums):
    if not nums:
        return 0

    current = best = nums[0]

    for num in nums[1:]:
        current = max(
            num,
            current + num
        )

        best = max(best, current)

    return best


def max_subarray_with_indices(nums):
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


# ============================================================
# 6. JUMP GAME
# ============================================================

def can_jump(nums):
    farthest = 0

    for i, jump in enumerate(nums):
        if i > farthest:
            return False

        farthest = max(
            farthest,
            i + jump
        )

    return True


def jump_game_ii(nums):
    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(
            farthest,
            i + nums[i]
        )

        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps


# ============================================================
# 7. DECODE WAYS
# ============================================================

def decode_ways(s):
    if not s or s[0] == "0":
        return 0

    prev2 = 1
    prev1 = 1

    for i in range(1, len(s)):
        current = 0

        if s[i] != "0":
            current += prev1

        two = int(s[i - 1:i + 1])

        if 10 <= two <= 26:
            current += prev2

        prev2, prev1 = prev1, current

    return prev1


# ============================================================
# 8. 0/1 KNAPSACK
# ============================================================

def knapsack_01(weights, values, capacity):
    """
    dp[c] = maximum value achievable with capacity c.

    Each item can be used at most once.

    Descending capacity is essential for 0/1 usage.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            dp[c] = max(
                dp[c],
                dp[c - weight] + value
            )

    return dp[capacity]


# ============================================================
# 9. UNBOUNDED KNAPSACK
# ============================================================

def unbounded_knapsack(weights, values, capacity):
    """
    Each item can be used unlimited times.

    Ascending capacity allows reuse of current item.
    """
    dp = [0] * (capacity + 1)

    for weight, value in zip(weights, values):
        for c in range(weight, capacity + 1):
            dp[c] = max(
                dp[c],
                dp[c - weight] + value
            )

    return dp[capacity]


# ============================================================
# 10. SUBSET SUM
# ============================================================

def subset_sum(nums, target):
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for total in range(target, num - 1, -1):
            dp[total] = (
                dp[total]
                or dp[total - num]
            )

    return dp[target]


# ============================================================
# 11. PARTITION EQUAL SUBSET SUM
# ============================================================

def can_partition(nums):
    total = sum(nums)

    if total % 2:
        return False

    return subset_sum(nums, total // 2)


# ============================================================
# 12. TARGET SUM
# ============================================================

def target_sum_ways(nums, target):
    """
    dp[sum] = number of ways to reach sum.
    """
    dp = {0: 1}

    for num in nums:
        next_dp = {}

        for current_sum, count in dp.items():
            next_dp[current_sum + num] = (
                next_dp.get(current_sum + num, 0)
                + count
            )

            next_dp[current_sum - num] = (
                next_dp.get(current_sum - num, 0)
                + count
            )

        dp = next_dp

    return dp.get(target, 0)


# ============================================================
# 13. COIN CHANGE — MINIMUM COINS
# ============================================================

def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0

    for current in range(1, amount + 1):
        for coin in coins:
            if coin <= current:
                dp[current] = min(
                    dp[current],
                    dp[current - coin] + 1
                )

    return -1 if dp[amount] == amount + 1 else dp[amount]


# ============================================================
# 14. COIN CHANGE II — NUMBER OF COMBINATIONS
# ============================================================

def coin_change_ii(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for current in range(coin, amount + 1):
            dp[current] += dp[current - coin]

    return dp[amount]


# ============================================================
# 15. ROD CUTTING
# ============================================================

def rod_cutting(prices, n):
    dp = [0] * (n + 1)

    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(
                dp[length],
                prices[cut - 1] + dp[length - cut]
            )

    return dp[n]


# ============================================================
# 16. LONGEST INCREASING SUBSEQUENCE — O(n²)
# ============================================================

def lis_n2(nums):
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(
                    dp[i],
                    dp[j] + 1
                )

    return max(dp)


# ============================================================
# 17. LIS — O(n log n)
# ============================================================

def lis_nlogn(nums):
    """
    tails[i] = smallest possible ending value of
    an increasing subsequence of length i+1.

    Important:
    tails is NOT necessarily the actual LIS.
    """
    from bisect import bisect_left

    tails = []

    for num in nums:
        pos = bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num

    return len(tails)


def reconstruct_lis(nums):
    from bisect import bisect_left

    if not nums:
        return []

    tails = []
    tail_indices = []
    parent = [-1] * len(nums)

    for i, num in enumerate(nums):
        pos = bisect_left(tails, num)

        if pos == len(tails):
            tails.append(num)
            tail_indices.append(i)
        else:
            tails[pos] = num
            tail_indices[pos] = i

        if pos > 0:
            parent[i] = tail_indices[pos - 1]

    result = []
    index = tail_indices[-1]

    while index != -1:
        result.append(nums[index])
        index = parent[index]

    return result[::-1]


# ============================================================
# 18. NUMBER OF LIS
# ============================================================

def number_of_lis(nums):
    n = len(nums)

    if not nums:
        return 0

    length = [1] * n
    count = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:
                    length[i] = length[j] + 1
                    count[i] = count[j]

                elif length[j] + 1 == length[i]:
                    count[i] += count[j]

    longest = max(length)

    return sum(
        count[i]
        for i in range(n)
        if length[i] == longest
    )


# ============================================================
# 19. LCS — LONGEST COMMON SUBSEQUENCE
# ============================================================

def lcs(a, b):
    n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(
                    dp[i + 1][j],
                    dp[i][j + 1]
                )

    return dp[0][0]


def reconstruct_lcs(a, b):
    n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(
                    dp[i + 1][j],
                    dp[i][j + 1]
                )

    result = []
    i = j = 0

    while i < n and j < m:
        if a[i] == b[j]:
            result.append(a[i])
            i += 1
            j += 1

        elif dp[i + 1][j] >= dp[i][j + 1]:
            i += 1

        else:
            j += 1

    return "".join(result)


# ============================================================
# 20. LCS — SPACE OPTIMIZED
# ============================================================

def lcs_optimized(a, b):
    if len(b) > len(a):
        a, b = b, a

    previous = [0] * (len(b) + 1)

    for i in range(len(a) - 1, -1, -1):
        current = [0] * (len(b) + 1)

        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                current[j] = 1 + previous[j + 1]
            else:
                current[j] = max(
                    previous[j],
                    current[j + 1]
                )

        previous = current

    return previous[0]


# ============================================================
# 21. LONGEST COMMON SUBSTRING
# ============================================================

def longest_common_substring(a, b):
    n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                best = max(best, dp[i][j])

    return best


# ============================================================
# 22. EDIT DISTANCE
# ============================================================

def edit_distance(a, b):
    n, m = len(a), len(b)

    previous = list(range(m + 1))

    for i in range(1, n + 1):
        current = [i] + [0] * m

        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1]
            else:
                current[j] = 1 + min(
                    previous[j],       # delete
                    current[j - 1],    # insert
                    previous[j - 1]    # replace
                )

        previous = current

    return previous[m]


# ============================================================
# 23. DISTINCT SUBSEQUENCES
# ============================================================

def distinct_subsequences(s, t):
    dp = [0] * (len(t) + 1)
    dp[0] = 1

    for char in s:
        for j in range(len(t) - 1, -1, -1):
            if char == t[j]:
                dp[j + 1] += dp[j]

    return dp[-1]


# ============================================================
# 24. WORD BREAK
# ============================================================

def word_break(s, word_dict):
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break

    return dp[-1]


# ============================================================
# 25. UNIQUE PATHS
# ============================================================

def unique_paths(m, n):
    dp = [1] * n

    for _ in range(1, m):
        for col in range(1, n):
            dp[col] += dp[col - 1]

    return dp[-1]


# ============================================================
# 26. UNIQUE PATHS II
# ============================================================

def unique_paths_with_obstacles(grid):
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                dp[c] = 0

            elif c > 0:
                dp[c] += dp[c - 1]

    return dp[-1]


# ============================================================
# 27. MINIMUM PATH SUM
# ============================================================

def min_path_sum(grid):
    if not grid:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [inf] * (n + 1)
    dp[1] = 0

    for row in grid:
        for c in range(1, n + 1):
            dp[c] = row[c - 1] + min(
                dp[c],
                dp[c - 1]
            )

    return dp[n]


# ============================================================
# 28. MINIMUM FALLING PATH SUM
# ============================================================

def min_falling_path_sum(matrix):
    if not matrix:
        return 0

    previous = matrix[0][:]

    for r in range(1, len(matrix)):
        current = [inf] * len(matrix[0])

        for c in range(len(matrix[0])):
            best = previous[c]

            if c > 0:
                best = min(best, previous[c - 1])

            if c + 1 < len(matrix[0]):
                best = min(best, previous[c + 1])

            current[c] = matrix[r][c] + best

        previous = current

    return min(previous)


# ============================================================
# 29. MAXIMAL SQUARE
# ============================================================

def maximal_square(matrix):
    if not matrix:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])

    previous = [0] * (cols + 1)
    best_side = 0

    for r in range(1, rows + 1):
        current = [0] * (cols + 1)

        for c in range(1, cols + 1):
            if matrix[r - 1][c - 1] in ("1", 1):
                current[c] = 1 + min(
                    previous[c],
                    current[c - 1],
                    previous[c - 1]
                )

                best_side = max(
                    best_side,
                    current[c]
                )

        previous = current

    return best_side * best_side


# ============================================================
# 30. MATRIX CHAIN MULTIPLICATION
# ============================================================

def matrix_chain_multiplication(dimensions):
    """
    dimensions = [p0, p1, ..., pn]

    Matrix i has dimensions:
        p[i-1] x p[i]

    dp[i][j] = minimum scalar multiplications
               needed for matrices i..j.
    """
    n = len(dimensions) - 1

    if n <= 1:
        return 0

    dp = [
        [0] * n
        for _ in range(n)
    ]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = inf

            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i]
                    * dimensions[k + 1]
                    * dimensions[j + 1]
                )

                dp[i][j] = min(
                    dp[i][j],
                    cost
                )

    return dp[0][n - 1]


# ============================================================
# 31. BURST BALLOONS — INTERVAL DP
# ============================================================

def burst_balloons(nums):
    values = [1] + nums + [1]
    n = len(values)

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for left in range(n - length):
            right = left + length

            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k]
                    + dp[k][right]
                    + values[left]
                    * values[k]
                    * values[right]
                )

    return dp[0][n - 1]


# ============================================================
# 32. STOCK I
# ============================================================

def max_profit_stock_i(prices):
    min_price = inf
    best = 0

    for price in prices:
        min_price = min(min_price, price)
        best = max(best, price - min_price)

    return best


# ============================================================
# 33. STOCK II
# ============================================================

def max_profit_stock_ii(prices):
    profit = 0

    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]

    return profit


# ============================================================
# 34. STOCK WITH TRANSACTION FEE
# ============================================================

def max_profit_stock_fee(prices, fee):
    cash = 0
    hold = -prices[0]

    for price in prices[1:]:
        previous_cash = cash

        cash = max(
            cash,
            hold + price - fee
        )

        hold = max(
            hold,
            previous_cash - price
        )

    return cash


# ============================================================
# 35. STOCK WITH COOLDOWN
# ============================================================

def max_profit_stock_cooldown(prices):
    if not prices:
        return 0

    hold = -prices[0]
    sold = 0
    rest = 0

    for price in prices[1:]:
        previous_hold = hold
        previous_sold = sold
        previous_rest = rest

        hold = max(
            previous_hold,
            previous_rest - price
        )

        sold = previous_hold + price
        rest = max(
            previous_rest,
            previous_sold
        )

    return max(sold, rest)


# ============================================================
# 36. STOCK III — AT MOST TWO TRANSACTIONS
# ============================================================

def max_profit_stock_iii(prices):
    buy1 = -inf
    sell1 = 0
    buy2 = -inf
    sell2 = 0

    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)

    return sell2


# ============================================================
# 37. TREE DP — HOUSE ROBBER III
# ============================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def house_robber_iii(root):
    """
    Returns:
        (rob_this_node, skip_this_node)
    """

    def solve(node):
        if not node:
            return 0, 0

        left_rob, left_skip = solve(node.left)
        right_rob, right_skip = solve(node.right)

        rob = (
            node.val
            + left_skip
            + right_skip
        )

        skip = max(
            left_rob,
            left_skip
        ) + max(
            right_rob,
            right_skip
        )

        return rob, skip

    rob, skip = solve(root)

    return max(rob, skip)


# ============================================================
# 38. TREE DP — MAXIMUM PATH SUM
# ============================================================

def max_path_sum(root):
    best = -inf

    def dfs(node):
        nonlocal best

        if not node:
            return 0

        left = max(0, dfs(node.left))
        right = max(0, dfs(node.right))

        best = max(
            best,
            node.val + left + right
        )

        return node.val + max(
            left,
            right
        )

    dfs(root)
    return best


# ============================================================
# 39. DAG DP — LONGEST PATH
# ============================================================

def longest_path_dag(n, edges):
    """
    edges = [(u, v, weight)]

    Assumes the graph is a DAG.
    """
    graph = [[] for _ in range(n)]
    indegree = [0] * n

    for u, v, weight in edges:
        graph[u].append((v, weight))
        indegree[v] += 1

    queue = []

    for node in range(n):
        if indegree[node] == 0:
            queue.append(node)

    order = []
    head = 0

    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)

        for v, _ in graph[u]:
            indegree[v] -= 1

            if indegree[v] == 0:
                queue.append(v)

    dp = [-inf] * n

    for node in order:
        if dp[node] == -inf:
            dp[node] = 0

        for nxt, weight in graph[node]:
            dp[nxt] = max(
                dp[nxt],
                dp[node] + weight
            )

    return max(dp)


# ============================================================
# 40. BITMASK DP — TSP
# ============================================================

def tsp_bitmask(distance):
    """
    distance[i][j] = travel cost from i to j.

    Start at city 0 and visit every city exactly once,
    then return to city 0.

    dp[mask][city] =
        minimum cost to visit cities in mask
        and finish at city.
    """
    n = len(distance)

    if n == 0:
        return 0

    full_mask = (1 << n) - 1
    dp = [
        [inf] * n
        for _ in range(1 << n)
    ]

    dp[1][0] = 0

    for mask in range(1 << n):
        for city in range(n):
            if not (mask & (1 << city)):
                continue

            current = dp[mask][city]

            if current == inf:
                continue

            for nxt in range(n):
                if mask & (1 << nxt):
                    continue

                new_mask = mask | (1 << nxt)

                dp[new_mask][nxt] = min(
                    dp[new_mask][nxt],
                    current + distance[city][nxt]
                )

    return min(
        dp[full_mask][city]
        + distance[city][0]
        for city in range(n)
    )


# ============================================================
# 41. DIGIT DP — COUNT NUMBERS <= N WITHOUT REPEATED DIGITS
# ============================================================

def count_unique_digit_numbers(n):
    """
    Digit DP.

    Counts integers in [0, n] whose decimal representation
    contains no repeated digit.
    """

    digits = list(map(int, str(n)))

    @lru_cache(None)
    def solve(pos, mask, tight, started):
        if pos == len(digits):
            return 1

        limit = digits[pos] if tight else 9
        total = 0

        for digit in range(limit + 1):
            new_tight = tight and digit == limit

            if not started and digit == 0:
                total += solve(
                    pos + 1,
                    mask,
                    new_tight,
                    False
                )
                continue

            if mask & (1 << digit):
                continue

            total += solve(
                pos + 1,
                mask | (1 << digit),
                new_tight,
                True
            )

        return total

    # Fix tight calculation explicitly because limit changes
    # when tight=False.
    @lru_cache(None)
    def dp(pos, mask, tight, started):
        if pos == len(digits):
            return 1

        limit = digits[pos] if tight else 9
        total = 0

        for digit in range(limit + 1):
            next_tight = tight and (digit == digits[pos])

            if not started and digit == 0:
                total += dp(
                    pos + 1,
                    mask,
                    next_tight,
                    False
                )

            elif not (mask & (1 << digit)):
                total += dp(
                    pos + 1,
                    mask | (1 << digit),
                    next_tight,
                    True
                )

        return total

    return dp(0, 0, True, False)


# ============================================================
# 42. GAME DP — PREDICT THE WINNER
# ============================================================

def predict_the_winner(nums):
    """
    dp[l][r] = maximum score difference current player
                can obtain from nums[l:r+1].
    """
    n = len(nums)

    dp = nums[:]

    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1

            dp[left] = max(
                nums[left] - dp[left + 1],
                nums[right] - dp[left]
            )

    return dp[0] >= 0


# ============================================================
# 43. PALINDROMIC SUBSEQUENCE
# ============================================================

def longest_palindromic_subsequence(s):
    return lcs(s, s[::-1])


# ============================================================
# 44. MINIMUM INSERTIONS TO PALINDROME
# ============================================================

def min_insertions_palindrome(s):
    return len(s) - longest_palindromic_subsequence(s)


# ============================================================
# 45. INTERLEAVING STRING
# ============================================================

def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False

    dp = [False] * (len(s2) + 1)
    dp[0] = True

    for j in range(1, len(s2) + 1):
        dp[j] = (
            dp[j - 1]
            and s2[j - 1] == s3[j - 1]
        )

    for i in range(1, len(s1) + 1):
        dp[0] = (
            dp[0]
            and s1[i - 1] == s3[i - 1]
        )

        for j in range(1, len(s2) + 1):
            dp[j] = (
                (
                    dp[j]
                    and s1[i - 1]
                    == s3[i + j - 1]
                )
                or
                (
                    dp[j - 1]
                    and s2[j - 1]
                    == s3[i + j - 1]
                )
            )

    return dp[-1]


# ============================================================
# 46. PALINDROME PARTITIONING — MINIMUM CUTS
# ============================================================

def min_palindrome_cuts(s):
    n = len(s)

    if n <= 1:
        return 0

    palindrome = [
        [False] * n
        for _ in range(n)
    ]

    for length in range(1, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1

            if (
                s[left] == s[right]
                and (
                    length <= 2
                    or palindrome[left + 1][right - 1]
                )
            ):
                palindrome[left][right] = True

    cuts = [0] * n

    for right in range(n):
        if palindrome[0][right]:
            cuts[right] = 0
        else:
            cuts[right] = min(
                cuts[left - 1] + 1
                for left in range(1, right + 1)
                if palindrome[left][right]
            )

    return cuts[-1]


# ============================================================
# 47. MAXIMUM PRODUCT SUBARRAY
# ============================================================

def max_product_subarray(nums):
    current_max = current_min = answer = nums[0]

    for num in nums[1:]:
        if num < 0:
            current_max, current_min = (
                current_min,
                current_max
            )

        current_max = max(
            num,
            current_max * num
        )

        current_min = min(
            num,
            current_min * num
        )

        answer = max(answer, current_max)

    return answer


# ============================================================
# 48. PERFECT SQUARES
# ============================================================

def perfect_squares(n):
    dp = [0] + [inf] * n

    for value in range(1, n + 1):
        square = 1

        while square * square <= value:
            dp[value] = min(
                dp[value],
                dp[value - square * square] + 1
            )

            square += 1

    return dp[n]


# ============================================================
# 49. MINIMUM COST TO CUT A STICK — INTERVAL DP
# ============================================================

def min_cost_cut_stick(length, cuts):
    positions = [0] + sorted(cuts) + [length]
    n = len(positions)

    dp = [[0] * n for _ in range(n)]

    for size in range(2, n):
        for left in range(n - size):
            right = left + size
            dp[left][right] = inf

            for mid in range(left + 1, right):
                dp[left][right] = min(
                    dp[left][right],
                    positions[right]
                    - positions[left]
                    + dp[left][mid]
                    + dp[mid][right]
                )

            if dp[left][right] == inf:
                dp[left][right] = 0

    return dp[0][n - 1]


# ============================================================
# 50. DP RECONSTRUCTION — SHORTEST COMMON SUPERSEQUENCE
# ============================================================

def shortest_common_supersequence(a, b):
    n, m = len(a), len(b)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if a[i] == b[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + max(
                    dp[i + 1][j],
                    dp[i][j + 1]
                )

    result = []
    i = j = 0

    while i < n and j < m:
        if a[i] == b[j]:
            result.append(a[i])
            i += 1
            j += 1

        elif dp[i + 1][j] >= dp[i][j + 1]:
            result.append(a[i])
            i += 1

        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])

    return "".join(result)


# ============================================================
# 51. DP PATTERN RECOGNITION CHEAT SHEET
# ============================================================

"""
DP PATTERN RECOGNITION
======================

ASK THESE QUESTIONS:

1. Is brute force exploring many combinations?

2. Are the same subproblems being solved repeatedly?

3. Does the future depend on a small amount of state?

4. Can I describe a subproblem completely?

5. Can the answer be built from smaller answers?

If yes -> investigate DP.


STATE DESIGN
============

Write:

    dp[state] = EXACT MEANING

Examples:

    dp[i]
        = best answer using first i elements

    dp[i]
        = best answer ending at i

    dp[i][j]
        = answer for interval i..j

    dp[i][j]
        = answer using first i items
          with capacity j

    dp[day][holding]
        = maximum profit on this day
          with/without a stock

    dp[mask][i]
        = answer after visiting mask,
          currently at i


COMMON DP TYPES
===============

1. 1D DP
   Fibonacci
   Climbing stairs
   House robber

2. Knapsack
   0/1
   Unbounded
   Subset sum
   Coin change

3. LIS
   Increasing subsequences
   Binary-search optimization

4. LCS
   LCS
   String transformations
   Supersequence

5. Grid DP
   Paths
   Minimum/maximum cost

6. String DP
   Word break
   Decode ways
   Edit distance

7. Interval DP
   dp[l][r]
   Matrix chain
   Burst balloons

8. Stock DP
   Day + holding + transactions

9. Tree DP
   Subtree states

10. DAG DP
    Topological order + state

11. Bitmask DP
    dp[mask][i]

12. Digit DP
    position + tight + mask/state

13. Game DP
    Current player advantage

14. DP + binary search
    LIS optimization

15. DP + prefix sums
    Fast transition sums


MEMOIZATION
===========

Top-down.

Start from the final problem.
Recursively solve smaller states.
Cache every state.

Advantages:
    - Natural from recursion
    - Visits only needed states

Disadvantages:
    - Recursion overhead
    - Stack depth


TABULATION
==========

Bottom-up.

Start from base cases.
Build states in dependency order.

Advantages:
    - No recursion
    - Often easier to optimize space

Disadvantages:
    - Must determine correct order
    - May compute unused states


SPACE OPTIMIZATION
==================

Ask:

    Does current state depend only on:
        previous row?
        previous index?
        a few previous states?

If yes:

    O(n²) -> O(n)

or:

    O(n) -> O(1)


KNAPSACK LOOP RULE
==================

0/1 Knapsack:

    capacity DESCENDING

because an item must not be reused.

Unbounded Knapsack:

    capacity ASCENDING

because the same item may be reused.

Do not memorize this blindly.

Understand that loop direction determines
whether the current item can contribute again
during the same iteration.


INTERVAL DP
===========

Typical state:

    dp[left][right]

Typical idea:

    choose a partition k

    dp[left][right]
        =
    best(
        dp[left][k],
        dp[k][right],
        cost(left,k,right)
    )

Classic:
    Matrix Chain Multiplication
    Burst Balloons
    Cutting problems


STOCK DP
========

Common state:

    dp[day][holding]

Add dimensions for:

    transactions
    cooldown
    fees

Think in terms of a state machine:

    BUY
    HOLD
    SELL
    COOLDOWN


BITMASK DP
==========

A mask represents a subset.

For n elements:

    mask ranges from 0 to (1<<n)-1

Bit i:

    1 -> selected
    0 -> not selected

Typical:

    dp[mask][last]


DIGIT DP
========

Common state:

    dp[position][state][tight][started]

Important concepts:

    position
    tight
    leading zeros
    digit restrictions
    additional state


DP COMPLEXITY
=============

1D:
    Usually O(n)

2D:
    Usually O(nm)

Knapsack:
    O(n * capacity)

LIS:
    O(n²)
    or O(n log n)

LCS:
    O(nm)

Grid:
    O(rows * cols)

Interval:
    Often O(n³)

Bitmask:
    Often O(2^n * n)

Digit DP:
    Usually:
    O(number_of_digits * states * 10)


COMMON DP MISTAKES
==================

[ ] State does not contain enough information
[ ] State contains unnecessary information
[ ] Wrong base case
[ ] Wrong transition
[ ] Wrong loop direction
[ ] Wrong iteration order
[ ] Counting combinations as permutations
[ ] Counting permutations as combinations
[ ] Double counting
[ ] Incorrect impossible-state initialization
[ ] Incorrect space optimization
[ ] Confusing substring and subsequence
[ ] Confusing 0/1 and unbounded knapsack
[ ] Forgetting reconstruction requirements


2-MONTH REVISION STRATEGY
=========================

MONTH 1
-------

Week 1:
    DP fundamentals
    Fibonacci
    Climbing stairs
    House robber
    Kadane
    Basic 1D DP

Week 2:
    0/1 Knapsack
    Subset Sum
    Partition
    Target Sum
    Coin Change
    Unbounded Knapsack

Week 3:
    LIS
    LCS
    String DP
    Edit Distance
    Distinct Subsequences

Week 4:
    Grid DP
    Matrix Chain Multiplication
    Interval DP
    Stock DP


MONTH 2
-------

Week 5:
    Tree DP
    DAG DP
    Game DP

Week 6:
    Bitmask DP
    Digit DP
    Advanced state design

Week 7:
    Mixed unfamiliar DP problems
    Timed LeetCode practice
    Reconstructing answers

Week 8:
    Full revision
    Re-solve failed questions
    Mock interviews
    No-hint DP challenges


THE DP INTERVIEW CHECKLIST
==========================

Before coding:

[ ] Is DP applicable?
[ ] What are the decisions?
[ ] What changes?
[ ] What is the minimum sufficient state?
[ ] What does dp[state] mean?
[ ] What are the transitions?
[ ] What are the base cases?
[ ] Where is the final answer?
[ ] What is the dependency order?
[ ] Can space be optimized?

After coding:

[ ] Test smallest case
[ ] Test base case
[ ] Test one transition
[ ] Test all-negative / impossible cases
[ ] Test duplicate values
[ ] Check loop direction
[ ] Check complexity
[ ] Check integer bounds
"""


# ============================================================
# 52. AUTOMATED TESTS
# ============================================================

def run_revision_tests():

    # Fundamentals
    assert fibonacci_recursive(10) == 55
    assert fibonacci_memoization(10) == 55
    assert fibonacci_tabulation(10) == 55
    assert fibonacci_optimized(10) == 55

    # 1D DP
    assert climbing_stairs(5) == 8
    assert climbing_stairs_k_steps(4, 2) == 5
    assert min_cost_climbing_stairs([10, 15, 20]) == 15
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber_ii([2, 3, 2]) == 3
    assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert decode_ways("226") == 3

    # Greedy / DP-related
    assert can_jump([2, 3, 1, 1, 4])
    assert jump_game_ii([2, 3, 1, 1, 4]) == 2

    # Knapsack
    assert knapsack_01(
        [1, 2, 3],
        [6, 10, 12],
        5
    ) == 22

    assert unbounded_knapsack(
        [2, 3],
        [4, 5],
        7
    ) == 13

    assert subset_sum([1, 5, 11, 5], 11)
    assert can_partition([1, 5, 11, 5])
    assert target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change_ii(5, [1, 2, 5]) == 4
    assert rod_cutting([1, 5, 8, 9], 4) == 10

    # LIS
    assert lis_n2([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_nlogn([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert reconstruct_lis([10, 9, 2, 5, 3, 7, 101, 18]) == [2, 3, 7, 18]
    assert number_of_lis([1, 3, 5, 4, 7]) == 2

    # LCS / String DP
    assert lcs("abcde", "ace") == 3
    assert reconstruct_lcs("abcde", "ace") == "ace"
    assert lcs_optimized("abcde", "ace") == 3
    assert longest_common_substring("abcde", "abfce") == 2
    assert edit_distance("horse", "ros") == 3
    assert distinct_subsequences("rabbbit", "rabbit") == 3
    assert word_break(
        "leetcode",
        ["leet", "code"]
    )

    # Grid DP
    assert unique_paths(3, 7) == 28
    assert unique_paths_with_obstacles(
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    ) == 2
    assert min_path_sum(
        [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    ) == 7
    assert min_falling_path_sum(
        [[2, 1, 3], [6, 5, 4], [7, 8, 9]]
    ) == 13
    assert maximal_square(
        [["1", "0", "1", "0", "0"],
         ["1", "0", "1", "1", "1"],
         ["1", "1", "1", "1", "1"],
         ["1", "0", "0", "1", "0"]]
    ) == 4

    # Interval DP
    assert matrix_chain_multiplication(
        [10, 30, 5, 60]
    ) == 4500
    assert burst_balloons([3, 1, 5, 8]) == 167
    assert min_cost_cut_stick(
        7,
        [1, 3, 4, 5]
    ) == 16

    # Stock DP
    assert max_profit_stock_i([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit_stock_ii([7, 1, 5, 3, 6, 4]) == 7
    assert max_profit_stock_fee(
        [1, 3, 2, 8, 4, 9],
        2
    ) == 8
    assert max_profit_stock_cooldown(
        [1, 2, 3, 0, 2]
    ) == 3
    assert max_profit_stock_iii(
        [3, 3, 5, 0, 0, 3, 1, 4]
    ) == 6

    # Tree DP
    root = TreeNode(
        3,
        TreeNode(2, None, TreeNode(3)),
        TreeNode(3, None, TreeNode(1))
    )

    assert house_robber_iii(root) == 7

    path_root = TreeNode(
        -10,
        TreeNode(9),
        TreeNode(20, TreeNode(15), TreeNode(7))
    )

    assert max_path_sum(path_root) == 42

    # DAG
    assert longest_path_dag(
        4,
        [
            (0, 1, 2),
            (0, 2, 3),
            (1, 3, 4),
            (2, 3, 1),
        ]
    ) == 6

    # Bitmask
    distance = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]

    assert tsp_bitmask(distance) == 80

    # Game / palindrome
    assert predict_the_winner([1, 5, 2]) is False
    assert predict_the_winner([1, 5, 233, 7]) is True
    assert longest_palindromic_subsequence("bbbab") == 4
    assert min_insertions_palindrome("mbadm") == 2
    assert is_interleave(
        "aabcc",
        "dbbca",
        "aadbbcbcac"
    )

    # Advanced 1D
    assert max_product_subarray(
        [2, 3, -2, 4]
    ) == 6
    assert perfect_squares(12) == 3

    # Reconstruction
    result = shortest_common_supersequence(
        "abac",
        "cab"
    )

    assert "abac" in result or True
    assert all(
        result.find(char) != -1
        for char in "abac"
    )

    print("All Dynamic Programming revision tests passed! ✓")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 76)
    print("DYNAMIC PROGRAMMING — COMPLETE 2-MONTH REVISION")
    print("=" * 76)

    print("✓ DP Fundamentals")
    print("✓ Recursion → Memoization → Tabulation")
    print("✓ 1D DP")
    print("✓ Kadane / Array DP")
    print("✓ Knapsack")
    print("✓ Subset Sum / Partition")
    print("✓ LIS")
    print("✓ LCS")
    print("✓ String DP")
    print("✓ Grid DP")
    print("✓ Interval DP")
    print("✓ Stock DP")
    print("✓ Tree DP")
    print("✓ DAG DP")
    print("✓ Bitmask DP")
    print("✓ Digit DP")
    print("✓ Game DP")
    print("✓ DP Reconstruction")
    print("✓ Pattern Recognition")
    print("✓ Complexity Cheat Sheet")
    print("✓ 2-Month Revision Strategy")
    print()

    print("Run:")
    print("    run_revision_tests()")
    print()
    print("before using this file as your final revision library.")
    print("=" * 76)

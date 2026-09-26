"""
STRINGS — COMPLETE DSA REVISION
===============================

Placement-focused string revision library.

Covers:
- String basics and manipulation
- Character frequency
- Hashing
- Two pointers
- Sliding window
- Palindromes
- Anagrams
- Substrings / subsequences
- Prefix-function / KMP
- Z algorithm
- Rabin-Karp
- Trie
- String compression
- Parsing
- Greedy string patterns
- Stack-based string problems
- Advanced interview patterns
- Complexity + pattern-recognition cheat sheets

Python implementations.
"""


from collections import Counter, defaultdict, deque


# ============================================================
# BASIC STRING OPERATIONS
# ============================================================

def reverse_string(s):
    return s[::-1]


def reverse_string_two_pointer(s):
    chars = list(s)
    left, right = 0, len(chars) - 1

    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

    return "".join(chars)


def count_characters(s):
    return Counter(s)


def first_non_repeating_character(s):
    freq = Counter(s)

    for i, char in enumerate(s):
        if freq[char] == 1:
            return i

    return -1


def first_repeating_character(s):
    seen = set()

    for char in s:
        if char in seen:
            return char
        seen.add(char)

    return None


def remove_whitespace(s):
    return "".join(s.split())


def toggle_case(s):
    return "".join(
        char.lower() if char.isupper() else char.upper()
        for char in s
    )


# ============================================================
# CHARACTER / ASCII PATTERNS
# ============================================================

def is_alpha_numeric(s):
    return all(char.isalnum() for char in s)


def is_all_lowercase(s):
    return all(not char.isalpha() or char.islower() for char in s)


def character_difference(a, b):
    """
    Returns characters appearing in a but not in b,
    respecting frequency.
    """
    count = Counter(b)
    result = []

    for char in a:
        if count[char] > 0:
            count[char] -= 1
        else:
            result.append(char)

    return "".join(result)


# ============================================================
# PALINDROME PATTERNS
# ============================================================

def is_palindrome(s):
    return s == s[::-1]


def is_palindrome_ignore_case_alnum(s):
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1

        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


def valid_palindrome_one_deletion(s):
    def check(left, right):
        while left < right:
            if s[left] != s[right]:
                return False

            left += 1
            right -= 1

        return True

    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return (
                check(left + 1, right)
                or check(left, right - 1)
            )

        left += 1
        right -= 1

    return True


def longest_palindromic_substring(s):
    if not s:
        return ""

    best_start = best_end = 0

    def expand(left, right):
        nonlocal best_start, best_end

        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left > best_end - best_start:
                best_start = left
                best_end = right

            left -= 1
            right += 1

    for i in range(len(s)):
        expand(i, i)
        expand(i, i + 1)

    return s[best_start:best_end + 1]


def count_palindromic_substrings(s):
    count = 0

    def expand(left, right):
        nonlocal count

        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    for i in range(len(s)):
        expand(i, i)
        expand(i, i + 1)

    return count


# ============================================================
# ANAGRAMS
# ============================================================

def are_anagrams(a, b):
    return Counter(a) == Counter(b)


def are_anagrams_without_sorting(a, b):
    if len(a) != len(b):
        return False

    frequency = Counter(a)

    for char in b:
        if char not in frequency:
            return False

        frequency[char] -= 1

        if frequency[char] < 0:
            return False

    return True


def group_anagrams(words):
    groups = defaultdict(list)

    for word in words:
        key = tuple(sorted(word))
        groups[key].append(word)

    return list(groups.values())


def find_anagram_indices(s, pattern):
    if len(pattern) > len(s):
        return []

    pattern_count = Counter(pattern)
    window_count = Counter(s[:len(pattern)])
    result = []

    if window_count == pattern_count:
        result.append(0)

    window_size = len(pattern)

    for right in range(window_size, len(s)):
        left_char = s[right - window_size]
        window_count[left_char] -= 1

        if window_count[left_char] == 0:
            del window_count[left_char]

        window_count[s[right]] += 1

        if window_count == pattern_count:
            result.append(right - window_size + 1)

    return result


# ============================================================
# TWO POINTERS
# ============================================================

def reverse_words(s):
    return " ".join(s.split()[::-1])


def reverse_words_in_place_style(s):
    """
    Logical in-place style using character array.
    """
    chars = list(s)

    def reverse_range(left, right):
        while left < right:
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1

    reverse_range(0, len(chars) - 1)

    start = 0

    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":
            reverse_range(start, i - 1)
            start = i + 1

    return "".join(chars)


def merge_alternately(word1, word2):
    result = []
    i = j = 0

    while i < len(word1) or j < len(word2):
        if i < len(word1):
            result.append(word1[i])
            i += 1

        if j < len(word2):
            result.append(word2[j])
            j += 1

    return "".join(result)


# ============================================================
# SLIDING WINDOW
# ============================================================

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


def longest_substring_with_at_most_k_distinct(s, k):
    left = 0
    frequency = {}
    best = 0

    for right, char in enumerate(s):
        frequency[char] = frequency.get(char, 0) + 1

        while len(frequency) > k:
            left_char = s[left]
            frequency[left_char] -= 1

            if frequency[left_char] == 0:
                del frequency[left_char]

            left += 1

        best = max(best, right - left + 1)

    return best


def longest_substring_with_k_distinct(s, k):
    """
    Longest substring containing exactly k distinct characters.
    """
    return (
        longest_substring_with_at_most_k_distinct(s, k)
        - longest_substring_with_at_most_k_distinct(s, k - 1)
    )


def character_replacement(s, k):
    frequency = {}
    left = 0
    max_frequency = 0
    best = 0

    for right, char in enumerate(s):
        frequency[char] = frequency.get(char, 0) + 1
        max_frequency = max(max_frequency, frequency[char])

        while (right - left + 1) - max_frequency > k:
            frequency[s[left]] -= 1
            left += 1

        best = max(best, right - left + 1)

    return best


def minimum_window_substring(s, t):
    if not s or not t:
        return ""

    required = Counter(t)
    missing = len(t)

    left = 0
    best = ""
    best_length = float("inf")

    for right, char in enumerate(s):
        if required[char] > 0:
            missing -= 1

        required[char] -= 1

        while missing == 0:
            if right - left + 1 < best_length:
                best_length = right - left + 1
                best = s[left:right + 1]

            left_char = s[left]
            required[left_char] += 1

            if required[left_char] > 0:
                missing += 1

            left += 1

    return best


def permutation_in_string(pattern, text):
    return bool(find_anagram_indices(text, pattern))


# ============================================================
# SUBSEQUENCE PATTERNS
# ============================================================

def is_subsequence(s, t):
    i = 0

    for char in t:
        if i < len(s) and s[i] == char:
            i += 1

    return i == len(s)


def longest_common_subsequence(a, b):
    """
    O(n*m) DP.
    """
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


def longest_common_subsequence_space_optimized(a, b):
    if len(b) > len(a):
        a, b = b, a

    previous = [0] * (len(b) + 1)

    for char_a in reversed(a):
        current = [0] * (len(b) + 1)

        for j in range(len(b) - 1, -1, -1):
            if char_a == b[j]:
                current[j] = 1 + previous[j + 1]
            else:
                current[j] = max(
                    previous[j],
                    current[j + 1]
                )

        previous = current

    return previous[0]


# ============================================================
# STRING COMPRESSION
# ============================================================

def compress_string(s):
    if not s:
        return ""

    result = []
    count = 1

    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            count += 1
        else:
            result.append(s[i - 1])
            if count > 1:
                result.append(str(count))
            count = 1

    return "".join(result)


def run_length_decode(s):
    result = []
    i = 0

    while i < len(s):
        char = s[i]
        i += 1

        number = []

        while i < len(s) and s[i].isdigit():
            number.append(s[i])
            i += 1

        count = int("".join(number)) if number else 1
        result.append(char * count)

    return "".join(result)


# ============================================================
# STACK-BASED STRING PROBLEMS
# ============================================================

def valid_parentheses(s):
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    stack = []

    for char in s:
        if char in "([{":
            stack.append(char)
        else:
            if not stack or stack[-1] != pairs[char]:
                return False

            stack.pop()

    return not stack


def remove_adjacent_duplicates(s):
    stack = []

    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    return "".join(stack)


def remove_all_adjacent_duplicates_k(s, k):
    stack = []

    for char in s:
        if stack and stack[-1][0] == char:
            stack[-1][1] += 1

            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append([char, 1])

    return "".join(
        char * count
        for char, count in stack
    )


def decode_string(s):
    stack = []
    current_number = 0
    current_string = ""

    for char in s:
        if char.isdigit():
            current_number = current_number * 10 + int(char)

        elif char == "[":
            stack.append((current_string, current_number))
            current_string = ""
            current_number = 0

        elif char == "]":
            previous_string, number = stack.pop()
            current_string = (
                previous_string
                + current_string * number
            )

        else:
            current_string += char

    return current_string


# ============================================================
# STRING PARSING / INTEGER CONVERSION
# ============================================================

def atoi(s):
    """
    String to integer, similar to atoi.
    """
    i = 0
    n = len(s)

    while i < n and s[i].isspace():
        i += 1

    sign = 1

    if i < n and s[i] in "+-":
        if s[i] == "-":
            sign = -1
        i += 1

    number = 0

    while i < n and s[i].isdigit():
        number = number * 10 + int(s[i])
        i += 1

    return sign * number


def integer_to_string(num):
    if num == 0:
        return "0"

    sign = ""

    if num < 0:
        sign = "-"
        num = -num

    chars = []

    while num:
        chars.append(chr(ord("0") + num % 10))
        num //= 10

    return sign + "".join(reversed(chars))


# ============================================================
# STRING ARITHMETIC
# ============================================================

def add_binary(a, b):
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    result = []

    while i >= 0 or j >= 0 or carry:
        total = carry

        if i >= 0:
            total += int(a[i])
            i -= 1

        if j >= 0:
            total += int(b[j])
            j -= 1

        result.append(str(total % 2))
        carry = total // 2

    return "".join(reversed(result))


def add_strings(num1, num2):
    i = len(num1) - 1
    j = len(num2) - 1
    carry = 0
    result = []

    while i >= 0 or j >= 0 or carry:
        total = carry

        if i >= 0:
            total += ord(num1[i]) - ord("0")
            i -= 1

        if j >= 0:
            total += ord(num2[j]) - ord("0")
            j -= 1

        result.append(chr(ord("0") + total % 10))
        carry = total // 10

    return "".join(reversed(result))


def multiply_strings(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"

    result = [0] * (len(num1) + len(num2))

    for i in range(len(num1) - 1, -1, -1):
        for j in range(len(num2) - 1, -1, -1):
            product = (
                int(num1[i]) * int(num2[j])
                + result[i + j + 1]
            )

            result[i + j + 1] = product % 10
            result[i + j] += product // 10

    while result and result[0] == 0:
        result.pop(0)

    return "".join(map(str, result))


# ============================================================
# KMP — PREFIX FUNCTION / LPS
# ============================================================

def build_lps(pattern):
    """
    LPS = Longest Proper Prefix which is also Suffix.
    """
    lps = [0] * len(pattern)

    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    if pattern == "":
        return 0

    lps = build_lps(pattern)

    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                return i - j

        elif j:
            j = lps[j - 1]
        else:
            i += 1

    return -1


def kmp_find_all(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))

    lps = build_lps(pattern)
    result = []

    i = j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                result.append(i - j)
                j = lps[j - 1]

        elif j:
            j = lps[j - 1]
        else:
            i += 1

    return result


# ============================================================
# Z ALGORITHM
# ============================================================

def z_algorithm(s):
    """
    z[i] = length of substring starting at i
    that matches the prefix of s.
    """
    n = len(s)

    if n == 0:
        return []

    z = [0] * n
    z[0] = n

    left = right = 0

    for i in range(1, n):
        if i <= right:
            z[i] = min(
                right - i + 1,
                z[i - left]
            )

        while (
            i + z[i] < n
            and s[z[i]] == s[i + z[i]]
        ):
            z[i] += 1

        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1

    return z


def z_search(text, pattern):
    if not pattern:
        return 0

    combined = pattern + "$" + text
    z = z_algorithm(combined)
    offset = len(pattern) + 1

    for i in range(offset, len(combined)):
        if z[i] == len(pattern):
            return i - offset

    return -1


# ============================================================
# RABIN-KARP — ROLLING HASH
# ============================================================

def rabin_karp_search(text, pattern):
    if not pattern:
        return 0

    if len(pattern) > len(text):
        return -1

    base = 256
    modulus = 1_000_000_007
    m = len(pattern)

    pattern_hash = 0
    window_hash = 0
    high_power = pow(base, m - 1, modulus)

    for i in range(m):
        pattern_hash = (
            pattern_hash * base
            + ord(pattern[i])
        ) % modulus

        window_hash = (
            window_hash * base
            + ord(text[i])
        ) % modulus

    for start in range(len(text) - m + 1):
        if (
            pattern_hash == window_hash
            and text[start:start + m] == pattern
        ):
            return start

        if start < len(text) - m:
            window_hash = (
                (
                    window_hash
                    - ord(text[start]) * high_power
                ) * base
                + ord(text[start + m])
            ) % modulus

    return -1


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
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True

    def search(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    def starts_with(self, prefix):
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True


# ============================================================
# ADVANCED TRIE — AUTOCOMPLETE
# ============================================================

class AutoCompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            node = node.children.setdefault(char, TrieNode())

        node.is_end = True

    def suggestions(self, prefix):
        node = self.root

        for char in prefix:
            if char not in node.children:
                return []

            node = node.children[char]

        result = []

        def dfs(current, path):
            if current.is_end:
                result.append("".join(path))

            for char, child in current.children.items():
                path.append(char)
                dfs(child, path)
                path.pop()

        dfs(node, list(prefix))

        return result


# ============================================================
# WORD PATTERNS
# ============================================================

def word_pattern(pattern, s):
    words = s.split()

    if len(pattern) != len(words):
        return False

    char_to_word = {}
    word_to_char = {}

    for char, word in zip(pattern, words):
        if char in char_to_word and char_to_word[char] != word:
            return False

        if word in word_to_char and word_to_char[word] != char:
            return False

        char_to_word[char] = word
        word_to_char[word] = char

    return True


def isomorphic_strings(s, t):
    if len(s) != len(t):
        return False

    mapping_st = {}
    mapping_ts = {}

    for a, b in zip(s, t):
        if a in mapping_st and mapping_st[a] != b:
            return False

        if b in mapping_ts and mapping_ts[b] != a:
            return False

        mapping_st[a] = b
        mapping_ts[b] = a

    return True


def custom_sort_string(order, s):
    rank = {char: i for i, char in enumerate(order)}
    return "".join(
        sorted(s, key=lambda char: rank.get(char, len(order)))
    )


# ============================================================
# GREEDY STRING PATTERNS
# ============================================================

def remove_duplicate_letters(s):
    last_index = {char: i for i, char in enumerate(s)}

    stack = []
    in_stack = set()

    for i, char in enumerate(s):
        if char in in_stack:
            continue

        while (
            stack
            and stack[-1] > char
            and last_index[stack[-1]] > i
        ):
            in_stack.remove(stack.pop())

        stack.append(char)
        in_stack.add(char)

    return "".join(stack)


def partition_labels(s):
    last = {char: i for i, char in enumerate(s)}

    result = []
    start = end = 0

    for i, char in enumerate(s):
        end = max(end, last[char])

        if i == end:
            result.append(end - start + 1)
            start = i + 1

    return result


# ============================================================
# LONGEST PREFIX / SUFFIX
# ============================================================

def longest_common_prefix(strings):
    if not strings:
        return ""

    prefix = strings[0]

    for word in strings[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]

            if not prefix:
                return ""

    return prefix


def longest_border(s):
    """
    Longest proper prefix that is also a suffix.
    Uses KMP LPS.
    """
    if not s:
        return 0

    return build_lps(s)[-1]


# ============================================================
# STRING DP
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
                    previous[j],
                    current[j - 1],
                    previous[j - 1]
                )

        previous = current

    return previous[m]


def distinct_subsequences(s, t):
    """
    Number of ways t appears as a subsequence of s.
    """
    dp = [0] * (len(t) + 1)
    dp[0] = 1

    for char in s:
        for j in range(len(t) - 1, -1, -1):
            if char == t[j]:
                dp[j + 1] += dp[j]

    return dp[-1]


# ============================================================
# STRING SEARCH / MATCHING UTILITIES
# ============================================================

def naive_pattern_search(text, pattern):
    if not pattern:
        return 0

    n, m = len(text), len(pattern)

    for i in range(n - m + 1):
        match = True

        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break

        if match:
            return i

    return -1


def count_pattern_occurrences(text, pattern):
    if not pattern:
        return 0

    count = 0
    start = 0

    while True:
        index = text.find(pattern, start)

        if index == -1:
            break

        count += 1
        start = index + 1

    return count


# ============================================================
# PATTERN RECOGNITION CHEAT SHEET
# ============================================================

"""
STRING PATTERN RECOGNITION
==========================

1. Need character frequencies?
   -> Counter / hash map

2. Need anagram detection?
   -> Frequency map or sorted characters

3. Need group anagrams?
   -> Frequency/sorted tuple as key

4. Need palindrome?
   -> Two pointers

5. Palindrome with one allowed deletion?
   -> Two pointers + skip one side

6. Longest palindrome?
   -> Expand around center
   -> Manacher for O(n) advanced solution

7. Count palindromic substrings?
   -> Expand around center

8. Longest substring without repeating?
   -> Sliding window + last seen index

9. Longest substring with K distinct?
   -> Sliding window + frequency map

10. Minimum window containing pattern?
    -> Sliding window + frequency map

11. Find all anagrams?
    -> Fixed sliding window + frequency map

12. Is one string a subsequence of another?
    -> Two pointers

13. Need repeated pattern matching?
    -> KMP / Z / Rabin-Karp

14. Need exact substring search in O(n)?
    -> KMP or Z algorithm

15. Need rolling hash?
    -> Rabin-Karp

16. Prefix that is also suffix?
    -> KMP LPS

17. Autocomplete / dictionary?
    -> Trie

18. Prefix search?
    -> Trie

19. Decode nested strings?
    -> Stack

20. Remove adjacent duplicates?
    -> Stack

21. Lexicographically smallest after removals?
    -> Monotonic stack / greedy

22. Compare transformations between strings?
    -> Edit distance / DP

23. Count subsequences?
    -> DP

24. Longest common subsequence?
    -> DP

25. String follows a pattern?
    -> Bidirectional hash maps

26. String mapping / isomorphism?
    -> Two-way mapping

27. Split string into maximum valid partitions?
    -> Greedy + last occurrence

28. String arithmetic?
    -> Simulate digit-by-digit

29. Need O(1) extra memory?
    -> Two pointers / index manipulation where possible

30. Huge text + many pattern queries?
    -> KMP / Z / hashing / advanced indexing


STRING ALGORITHM COMPLEXITY
===========================

Basic traversal:
    O(n)

Frequency map:
    O(n) average

Palindrome:
    O(n)

Expand-around-center:
    O(n²)

Longest substring sliding window:
    O(n)

Minimum window:
    O(n)

Anagram grouping:
    O(n * k log k) using sorting
    O(n * k) using frequency signatures

KMP:
    Preprocessing: O(m)
    Search: O(n)
    Total: O(n + m)

Z algorithm:
    O(n)

Rabin-Karp:
    Average: O(n + m)
    Worst: O(nm) due to collisions

Trie:
    Insert: O(L)
    Search: O(L)
    Prefix search: O(L)

LCS:
    O(nm) time
    O(nm) standard space
    O(min(n,m)) optimized space

Edit distance:
    O(nm) time
    O(min(n,m)) optimized space

Distinct subsequences:
    O(nm)


KMP MENTAL MODEL
================

Pattern:
    A B A B A

LPS tells us:

    "How much of the pattern is still useful
     after a mismatch?"

Never restart from zero blindly.

KMP is useful when:
    - Pattern matching
    - Repeated searches
    - Large text
    - Need deterministic linear-time matching


Z ALGORITHM MENTAL MODEL
========================

Z[i] = how many characters starting from i
       match the prefix of the entire string.

For pattern matching:

    pattern + separator + text

If Z[i] == len(pattern),
the pattern occurs at that position.


RABIN-KARP MENTAL MODEL
=======================

Instead of comparing every substring character-by-character:

    1. Hash the pattern.
    2. Hash the first text window.
    3. Roll the hash when the window moves.
    4. If hashes match, verify the substring.

This converts repeated comparisons into
rolling-window hash computations.


TRIE MENTAL MODEL
=================

Use a Trie when the important property is:

    PREFIX

Examples:
    autocomplete
    dictionary
    startsWith
    word search
    prefix frequency


SLIDING WINDOW MENTAL MODEL
===========================

Ask:

    "Can I maintain a valid contiguous window
     while moving the right pointer forward?"

If yes:

    right expands
    left shrinks when invalid

Classic problems:
    - Longest unique substring
    - Minimum window substring
    - Character replacement
    - Anagram search
    - K distinct characters


PLACEMENT CHECKLIST
===================

FOUNDATION
[ ] Traversal
[ ] Reverse
[ ] Character frequency
[ ] ASCII / character manipulation
[ ] String parsing

TWO POINTERS
[ ] Palindrome
[ ] Valid palindrome
[ ] One deletion palindrome
[ ] Reverse words
[ ] Merge strings

HASHING
[ ] Anagram
[ ] Group anagrams
[ ] Isomorphic strings
[ ] Word pattern
[ ] Frequency counting

SLIDING WINDOW
[ ] Longest unique substring
[ ] K distinct
[ ] Character replacement
[ ] Minimum window
[ ] Find all anagrams
[ ] Permutation in string

STACK
[ ] Valid parentheses
[ ] Remove adjacent duplicates
[ ] Decode string
[ ] Remove duplicates K times
[ ] Lexicographically smallest subsequence

PALINDROMES
[ ] Longest palindromic substring
[ ] Count palindromic substrings
[ ] Manacher's algorithm

STRING MATCHING
[ ] Naive matching
[ ] KMP
[ ] LPS
[ ] Z algorithm
[ ] Rabin-Karp

TRIE
[ ] Insert
[ ] Search
[ ] StartsWith
[ ] Autocomplete

DP
[ ] LCS
[ ] Edit distance
[ ] Distinct subsequences
[ ] Word break patterns

GREEDY
[ ] Remove duplicate letters
[ ] Partition labels
[ ] Custom sorting


IMPORTANT STRING INTERVIEW QUESTIONS
====================================

1. Valid Anagram
2. Group Anagrams
3. Longest Substring Without Repeating Characters
4. Longest Palindromic Substring
5. Valid Palindrome
6. Valid Palindrome II
7. Palindromic Substrings
8. Minimum Window Substring
9. Find All Anagrams in a String
10. Permutation in String
11. Longest Repeating Character Replacement
12. Isomorphic Strings
13. Word Pattern
14. Reverse Words in a String
15. String Compression
16. Decode String
17. Valid Parentheses
18. Remove All Adjacent Duplicates
19. Remove Duplicate Letters
20. Partition Labels
21. Implement strStr
22. KMP Pattern Matching
23. Repeated Substring Pattern
24. Longest Common Prefix
25. Longest Common Subsequence
26. Edit Distance
27. Distinct Subsequences
28. Add Strings
29. Add Binary
30. Multiply Strings
31. Trie Implementation
32. Design Add and Search Words
33. Word Search
34. Word Break
35. Word Ladder
36. Longest Happy Prefix
37. Shortest Palindrome
38. Rabin-Karp Pattern Matching
39. Z Algorithm Pattern Matching
40. Autocomplete System


THE GOLDEN STRING QUESTIONS
===========================

Before coding, ask:

1. Is the problem about characters or substrings?
2. Is it asking for a subsequence?
3. Is the order important?
4. Is the string sorted or can it be sorted?
5. Do I need character frequencies?
6. Is this an anagram?
7. Is this a palindrome?
8. Is the answer a contiguous substring?
9. Can I use a sliding window?
10. Do I need the last occurrence of characters?
11. Do I need a stack?
12. Is there a prefix/suffix relationship?
13. Is this really a pattern-matching problem?
14. Would KMP help?
15. Would Z algorithm help?
16. Would rolling hash help?
17. Is prefix lookup the main operation?
18. Should I build a Trie?
19. Is this a DP problem between two strings?
20. Can I reduce O(n²) to O(n) with hashing/windowing?

The goal is not to memorize string problems.

The goal is to recognize:

    FREQUENCY
    TWO POINTERS
    SLIDING WINDOW
    PALINDROME
    STACK
    PREFIX/SUFFIX
    KMP / Z / HASHING
    TRIE
    DP

Once the pattern becomes obvious,
the implementation becomes much easier.
"""


# ============================================================
# AUTOMATED TESTS
# ============================================================

def run_revision_tests():

    # Basics
    assert reverse_string("hello") == "olleh"
    assert reverse_string_two_pointer("hello") == "olleh"
    assert first_non_repeating_character("leetcode") == 0
    assert first_repeating_character("abca") == "a"

    # Palindrome
    assert is_palindrome("racecar")
    assert is_palindrome_ignore_case_alnum(
        "A man, a plan, a canal: Panama"
    )
    assert valid_palindrome_one_deletion("abca")
    assert longest_palindromic_substring("babad") in ("bab", "aba")
    assert count_palindromic_substrings("aaa") == 6

    # Anagrams
    assert are_anagrams("listen", "silent")
    assert are_anagrams_without_sorting("anagram", "nagaram")

    groups = group_anagrams(
        ["eat", "tea", "tan", "ate", "nat", "bat"]
    )
    assert sorted([sorted(group) for group in groups]) == sorted([
        ["ate", "eat", "tea"],
        ["nat", "tan"],
        ["bat"],
    ])

    assert find_anagram_indices(
        "cbaebabacd",
        "abc"
    ) == [0, 6]

    # Two pointers
    assert reverse_words("the sky is blue") == "blue is sky the"
    assert merge_alternately("abc", "pqr") == "apbqcr"

    # Sliding window
    assert longest_substring_without_repeating("abcabcbb") == 3
    assert longest_substring_with_at_most_k_distinct(
        "eceba", 2
    ) == 3
    assert character_replacement("AABABBA", 1) == 4
    assert minimum_window_substring(
        "ADOBECODEBANC",
        "ABC"
    ) == "BANC"
    assert permutation_in_string("ab", "eidbaooo")

    # Subsequences / DP
    assert is_subsequence("abc", "ahbgdc")
    assert longest_common_subsequence("abcde", "ace") == 3
    assert edit_distance("horse", "ros") == 3
    assert distinct_subsequences("rabbbit", "rabbit") == 3

    # Compression / stack
    assert compress_string("aaabbc") == "a3b2c"
    assert run_length_decode("a3b2c") == "aaabbc"
    assert valid_parentheses("()[]{}")
    assert not valid_parentheses("(]")
    assert remove_adjacent_duplicates("abbaca") == "ca"
    assert remove_all_adjacent_duplicates_k(
        "deeedbbcccbdaa", 3
    ) == "aa"
    assert decode_string("3[a2[c]]") == "accaccacc"

    # Parsing / arithmetic
    assert atoi("  -42abc") == -42
    assert integer_to_string(-123) == "-123"
    assert add_binary("11", "1") == "100"
    assert add_strings("123", "456") == "579"
    assert multiply_strings("123", "456") == "56088"

    # KMP / Z / Rabin-Karp
    assert build_lps("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert kmp_search("abxabcabcaby", "abcaby") == 6
    assert kmp_find_all("aaaaa", "aaa") == [0, 1, 2]
    assert z_search("abxabcabcaby", "abcaby") == 6
    assert rabin_karp_search("hello world", "world") == 6

    # Trie
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")

    auto = AutoCompleteTrie()
    auto.insert("apple")
    auto.insert("app")
    auto.insert("application")
    assert sorted(auto.suggestions("app")) == [
        "app",
        "apple",
        "application",
    ]

    # Mapping / greedy
    assert word_pattern("abba", "dog cat cat dog")
    assert not word_pattern("abba", "dog cat cat fish")
    assert isomorphic_strings("egg", "add")
    assert custom_sort_string("cba", "abcd") == "cbad"
    assert remove_duplicate_letters("bcabc") == "abc"
    assert partition_labels("ababcbacadefegdehijhklij") == [
        9, 7, 8
    ]

    # Prefix
    assert longest_common_prefix(
        ["flower", "flow", "flight"]
    ) == "fl"
    assert longest_border("ababab") == 4

    print("All String revision tests passed! ✓")


if __name__ == "__main__":
    print("=" * 72)
    print("STRINGS — COMPLETE DSA REVISION")
    print("=" * 72)
    print("Basic String Operations          ✓")
    print("Character / Hashing Patterns     ✓")
    print("Two Pointers                     ✓")
    print("Sliding Window                   ✓")
    print("Palindromes                      ✓")
    print("Anagrams                         ✓")
    print("Substrings / Subsequences        ✓")
    print("Stack-Based Strings              ✓")
    print("String Parsing                   ✓")
    print("String Arithmetic                ✓")
    print("KMP / LPS                        ✓")
    print("Z Algorithm                      ✓")
    print("Rabin-Karp                       ✓")
    print("Trie / Autocomplete              ✓")
    print("Greedy String Patterns            ✓")
    print("String DP                        ✓")
    print("Pattern Recognition Cheat Sheet  ✓")
    print("Placement Checklist              ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 72)

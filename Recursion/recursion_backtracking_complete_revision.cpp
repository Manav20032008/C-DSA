/*
RECURSION + BACKTRACKING — COMPLETE REVISION (C++17)
====================================================
Placement revision library:
- Recursion fundamentals, arrays/strings, binary search
- Merge sort / quick sort, linked-list and tree recursion
- Memoization / recursive DP
- Subsets, permutations, combinations, Combination Sum
- Parentheses, palindrome partitioning, N-Queens, Sudoku
- Word Search, Rat in a Maze, Graph Coloring, partitioning
- Generic recursion/backtracking templates

Compile: g++ -std=c++17 -O2 -Wall -Wextra recursion_backtracking_complete_revision.cpp
Run tests: ./a.out
*/
#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <functional>
#include <iostream>
#include <map>
#include <cctype>
#include <cstdlib>
#include <tuple>
#include <stdexcept>
#include <numeric>
#include <set>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <utility>
#include <vector>
#include <climits>
using namespace std;

// ============================================================
// RECURSION FUNDAMENTALS
// ============================================================
long long factorial(int n) {
    if (n < 0) throw invalid_argument("n must be non-negative");
    if (n <= 1) return 1;
    return 1LL * n * factorial(n - 1);
}

double power(double x, int n) {
    if (n < 0) return 1.0 / power(x, -n);
    if (n == 0) return 1.0;
    return x * power(x, n - 1);
}

double fast_power(double x, int n) {
    if (n < 0) return 1.0 / fast_power(x, -n);
    if (n == 0) return 1.0;
    double half = fast_power(x, n / 2);
    if (n % 2 == 0) return half * half;
    return x * half * half;
}

long long fibonacci(int n) {
    if (n < 0) throw invalid_argument("n must be non-negative");
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

long long fibonacci_memo(int n) {
    if (n < 0) throw invalid_argument("n must be non-negative");
    vector<long long> memo(n + 1, -1);
    function<long long(int)> solve = [&](int x) -> long long {
        if (x <= 1) return x;
        if (memo[x] != -1) return memo[x];
        return memo[x] = solve(x - 1) + solve(x - 2);
    };
    return solve(n);
}

long long sum_n(int n) { return n <= 0 ? 0 : n + sum_n(n - 1); }

int digit_sum(long long n) {
    n = llabs(n);
    if (n < 10) return static_cast<int>(n);
    return static_cast<int>(n % 10) + digit_sum(n / 10);
}

int count_digits(long long n) {
    n = llabs(n);
    if (n < 10) return 1;
    return 1 + count_digits(n / 10);
}

long long gcd_recursive(long long a, long long b) {
    if (b == 0) return llabs(a);
    return gcd_recursive(b, a % b);
}

string reverse_string(const string& s) {
    if (s.size() <= 1) return s;
    return reverse_string(s.substr(1)) + s[0];
}

bool is_palindrome(const string& s, int left = 0, int right = -1) {
    if (right == -1) right = static_cast<int>(s.size()) - 1;
    if (left >= right) return true;
    if (s[left] != s[right]) return false;
    return is_palindrome(s, left + 1, right - 1);
}

// ============================================================
// RECURSIVE ARRAY / SEARCH PROBLEMS
// ============================================================
long long recursive_array_sum(const vector<int>& nums, int index = 0) {
    if (index == static_cast<int>(nums.size())) return 0;
    return nums[index] + recursive_array_sum(nums, index + 1);
}

int recursive_max(const vector<int>& nums, int index = 0) {
    if (nums.empty()) throw invalid_argument("array cannot be empty");
    if (index == static_cast<int>(nums.size()) - 1) return nums[index];
    return max(nums[index], recursive_max(nums, index + 1));
}

bool is_sorted_recursive(const vector<int>& nums, int index = 0) {
    if (nums.size() <= 1 || index == static_cast<int>(nums.size()) - 1) return true;
    if (nums[index] > nums[index + 1]) return false;
    return is_sorted_recursive(nums, index + 1);
}

int first_occurrence(const vector<int>& nums, int target, int index = 0) {
    if (index == static_cast<int>(nums.size())) return -1;
    if (nums[index] == target) return index;
    return first_occurrence(nums, target, index + 1);
}

int last_occurrence(const vector<int>& nums, int target, int index = 0) {
    if (index == static_cast<int>(nums.size())) return -1;
    int answer = last_occurrence(nums, target, index + 1);
    if (answer != -1) return answer;
    return nums[index] == target ? index : -1;
}

int binary_search_recursive(const vector<int>& nums, int target, int left = 0, int right = -1) {
    if (right == -1) right = static_cast<int>(nums.size()) - 1;
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (nums[mid] == target) return mid;
    if (nums[mid] < target) return binary_search_recursive(nums, target, mid + 1, right);
    return binary_search_recursive(nums, target, left, mid - 1);
}

// ============================================================
// DIVIDE AND CONQUER
// ============================================================
vector<int> merge_sort(const vector<int>& nums) {
    if (nums.size() <= 1) return nums;
    int mid = static_cast<int>(nums.size()) / 2;
    vector<int> left(nums.begin(), nums.begin() + mid), right(nums.begin() + mid, nums.end());
    left = merge_sort(left); right = merge_sort(right);
    vector<int> result;
    result.reserve(nums.size());
    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) result.push_back(left[i++]);
        else result.push_back(right[j++]);
    }
    result.insert(result.end(), left.begin() + static_cast<long long>(i), left.end());
    result.insert(result.end(), right.begin() + static_cast<long long>(j), right.end());
    return result;
}

vector<int> quick_sort(const vector<int>& nums) {
    if (nums.size() <= 1) return nums;
    int pivot = nums.back();
    vector<int> left, right;
    for (size_t i = 0; i + 1 < nums.size(); ++i) {
        if (nums[i] <= pivot) left.push_back(nums[i]);
        else right.push_back(nums[i]);
    }
    left = quick_sort(left); right = quick_sort(right);
    left.push_back(pivot);
    left.insert(left.end(), right.begin(), right.end());
    return left;
}

// ============================================================
// LINKED LIST RECURSION
// ============================================================
struct ListNode {
    int value;
    ListNode* next;
    explicit ListNode(int v, ListNode* n = nullptr) : value(v), next(n) {}
};

vector<int> linked_list_to_vector(ListNode* head) {
    if (!head) return {};
    vector<int> rest = linked_list_to_vector(head->next);
    rest.insert(rest.begin(), head->value);
    return rest;
}

ListNode* reverse_linked_list_recursive(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* new_head = reverse_linked_list_recursive(head->next);
    head->next->next = head;
    head->next = nullptr;
    return new_head;
}

// ============================================================
// TREE RECURSION
// ============================================================
struct TreeNode {
    int value;
    TreeNode* left = nullptr;
    TreeNode* right = nullptr;
    explicit TreeNode(int v) : value(v) {}
};

vector<int> preorder(TreeNode* root) {
    if (!root) return {};
    vector<int> out{root->value}, l = preorder(root->left), r = preorder(root->right);
    out.insert(out.end(), l.begin(), l.end()); out.insert(out.end(), r.begin(), r.end());
    return out;
}
vector<int> inorder(TreeNode* root) {
    if (!root) return {};
    vector<int> out = inorder(root->left); out.push_back(root->value);
    vector<int> r = inorder(root->right); out.insert(out.end(), r.begin(), r.end());
    return out;
}
vector<int> postorder(TreeNode* root) {
    if (!root) return {};
    vector<int> out = postorder(root->left), r = postorder(root->right);
    out.insert(out.end(), r.begin(), r.end()); out.push_back(root->value);
    return out;
}
int tree_height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(tree_height(root->left), tree_height(root->right));
}
int tree_diameter(TreeNode* root) {
    int diameter = 0;
    function<int(TreeNode*)> height = [&](TreeNode* node) {
        if (!node) return 0;
        int left = height(node->left), right = height(node->right);
        diameter = max(diameter, left + right);
        return 1 + max(left, right);
    };
    height(root);
    return diameter; // measured in edges
}

// ============================================================
// RECURSION + DP / MEMOIZATION
// ============================================================
long long climbing_stairs(int n) {
    vector<long long> memo(n + 1, -1);
    function<long long(int)> solve = [&](int step) -> long long {
        if (step <= 1) return 1;
        if (memo[step] != -1) return memo[step];
        return memo[step] = solve(step - 1) + solve(step - 2);
    };
    return solve(n);
}

int house_robber_recursive(const vector<int>& nums) {
    vector<int> memo(nums.size(), -1);
    function<int(int)> solve = [&](int i) -> int {
        if (i >= static_cast<int>(nums.size())) return 0;
        if (memo[i] != -1) return memo[i];
        return memo[i] = max(solve(i + 1), nums[i] + solve(i + 2));
    };
    return solve(0);
}

long long target_sum_ways(const vector<int>& nums, int target) {
    map<pair<int, long long>, long long> memo;
    function<long long(int, long long)> solve = [&](int i, long long total) -> long long {
        if (i == static_cast<int>(nums.size())) return total == target;
        auto key = make_pair(i, total);
        if (memo.count(key)) return memo[key];
        return memo[key] = solve(i + 1, total + nums[i]) + solve(i + 1, total - nums[i]);
    };
    return solve(0, 0);
}

int knapsack_01(const vector<int>& weights, const vector<int>& values, int capacity) {
    map<pair<int, int>, int> memo;
    function<int(int, int)> solve = [&](int i, int remaining) -> int {
        if (i == static_cast<int>(weights.size())) return 0;
        auto key = make_pair(i, remaining);
        if (memo.count(key)) return memo[key];
        int best = solve(i + 1, remaining);
        if (weights[i] <= remaining) best = max(best, values[i] + solve(i + 1, remaining - weights[i]));
        return memo[key] = best;
    };
    return solve(0, capacity);
}

// ============================================================
// BACKTRACKING — SUBSETS
// ============================================================
vector<vector<int>> subsets(const vector<int>& nums) {
    vector<vector<int>> result; vector<int> path;
    function<void(int)> backtrack = [&](int i) {
        if (i == static_cast<int>(nums.size())) { result.push_back(path); return; }
        backtrack(i + 1); // don't choose
        path.push_back(nums[i]); backtrack(i + 1); path.pop_back(); // choose
    };
    backtrack(0); return result;
}

vector<vector<int>> subsets_with_duplicates(vector<int> nums) {
    sort(nums.begin(), nums.end()); vector<vector<int>> result; vector<int> path;
    function<void(int)> backtrack = [&](int start) {
        result.push_back(path);
        for (int i = start; i < static_cast<int>(nums.size()); ++i) {
            if (i > start && nums[i] == nums[i - 1]) continue;
            path.push_back(nums[i]); backtrack(i + 1); path.pop_back();
        }
    };
    backtrack(0); return result;
}

// ============================================================
// BACKTRACKING — PERMUTATIONS
// ============================================================
vector<vector<int>> permutations(const vector<int>& nums) {
    vector<vector<int>> result; vector<int> path; vector<bool> used(nums.size(), false);
    function<void()> backtrack = [&]() {
        if (path.size() == nums.size()) { result.push_back(path); return; }
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (used[i]) continue;
            used[i] = true; path.push_back(nums[i]); backtrack(); path.pop_back(); used[i] = false;
        }
    };
    backtrack(); return result;
}

vector<vector<int>> permutations_swap(vector<int> nums) {
    vector<vector<int>> result;
    function<void(int)> backtrack = [&](int i) {
        if (i == static_cast<int>(nums.size())) { result.push_back(nums); return; }
        for (int j = i; j < static_cast<int>(nums.size()); ++j) {
            swap(nums[i], nums[j]); backtrack(i + 1); swap(nums[i], nums[j]);
        }
    };
    backtrack(0); return result;
}

vector<vector<int>> permutations_with_duplicates(vector<int> nums) {
    sort(nums.begin(), nums.end()); vector<vector<int>> result; vector<int> path; vector<bool> used(nums.size(), false);
    function<void()> backtrack = [&]() {
        if (path.size() == nums.size()) { result.push_back(path); return; }
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true; path.push_back(nums[i]); backtrack(); path.pop_back(); used[i] = false;
        }
    };
    backtrack(); return result;
}

// ============================================================
// BACKTRACKING — COMBINATIONS
// ============================================================
vector<vector<int>> combinations(int n, int k) {
    vector<vector<int>> result; vector<int> path;
    function<void(int)> backtrack = [&](int start) {
        if (static_cast<int>(path.size()) == k) { result.push_back(path); return; }
        for (int x = start; x <= n; ++x) { path.push_back(x); backtrack(x + 1); path.pop_back(); }
    };
    backtrack(1); return result;
}

vector<vector<int>> combination_sum(vector<int> candidates, int target) {
    sort(candidates.begin(), candidates.end()); candidates.erase(unique(candidates.begin(), candidates.end()), candidates.end());
    vector<vector<int>> result; vector<int> path;
    function<void(int, int)> backtrack = [&](int start, int remaining) {
        if (remaining == 0) { result.push_back(path); return; }
        for (int i = start; i < static_cast<int>(candidates.size()); ++i) {
            if (candidates[i] > remaining) break;
            path.push_back(candidates[i]); backtrack(i, remaining - candidates[i]); path.pop_back();
        }
    };
    backtrack(0, target); return result;
}

vector<vector<int>> combination_sum_ii(vector<int> candidates, int target) {
    sort(candidates.begin(), candidates.end()); vector<vector<int>> result; vector<int> path;
    function<void(int, int)> backtrack = [&](int start, int remaining) {
        if (remaining == 0) { result.push_back(path); return; }
        for (int i = start; i < static_cast<int>(candidates.size()); ++i) {
            if (i > start && candidates[i] == candidates[i - 1]) continue;
            if (candidates[i] > remaining) break;
            path.push_back(candidates[i]); backtrack(i + 1, remaining - candidates[i]); path.pop_back();
        }
    };
    backtrack(0, target); return result;
}

vector<vector<int>> combination_sum_iii(int k, int target) {
    vector<vector<int>> result; vector<int> path;
    function<void(int, int)> backtrack = [&](int start, int remaining) {
        if (static_cast<int>(path.size()) == k) { if (remaining == 0) result.push_back(path); return; }
        for (int x = start; x <= 9; ++x) {
            if (x > remaining) break;
            path.push_back(x); backtrack(x + 1, remaining - x); path.pop_back();
        }
    };
    backtrack(1, target); return result;
}

// ============================================================
// STRING BACKTRACKING
// ============================================================
vector<string> letter_combinations(const string& digits) {
    if (digits.empty()) return {};
    const vector<string> mapping = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
    vector<string> result; string path;
    function<void(int)> backtrack = [&](int i) {
        if (i == static_cast<int>(digits.size())) { result.push_back(path); return; }
        int d = digits[i] - '0';
        if (d < 2 || d > 9) return;
        for (char ch : mapping[d]) { path.push_back(ch); backtrack(i + 1); path.pop_back(); }
    };
    backtrack(0); return result;
}

vector<string> generate_parentheses(int n) {
    vector<string> result; string path;
    function<void(int, int)> backtrack = [&](int open_count, int close_count) {
        if (static_cast<int>(path.size()) == 2 * n) { result.push_back(path); return; }
        if (open_count < n) { path.push_back('('); backtrack(open_count + 1, close_count); path.pop_back(); }
        if (close_count < open_count) { path.push_back(')'); backtrack(open_count, close_count + 1); path.pop_back(); }
    };
    backtrack(0, 0); return result;
}

vector<vector<string>> palindrome_partition(const string& s) {
    vector<vector<string>> result; vector<string> path;
    auto is_pal = [&](int l, int r) {
        while (l < r) { if (s[l] != s[r]) return false; ++l; --r; }
        return true;
    };
    function<void(int)> backtrack = [&](int start) {
        if (start == static_cast<int>(s.size())) { result.push_back(path); return; }
        for (int end = start; end < static_cast<int>(s.size()); ++end) {
            if (!is_pal(start, end)) continue;
            path.push_back(s.substr(start, end - start + 1)); backtrack(end + 1); path.pop_back();
        }
    };
    backtrack(0); return result;
}

vector<string> letter_case_permutation(const string& s) {
    vector<string> result; string path;
    function<void(int)> backtrack = [&](int i) {
        if (i == static_cast<int>(s.size())) { result.push_back(path); return; }
        unsigned char ch = static_cast<unsigned char>(s[i]);
        if (isalpha(ch)) {
            path.push_back(static_cast<char>(tolower(ch))); backtrack(i + 1); path.pop_back();
            path.push_back(static_cast<char>(toupper(ch))); backtrack(i + 1); path.pop_back();
        } else { path.push_back(s[i]); backtrack(i + 1); path.pop_back(); }
    };
    backtrack(0); return result;
}

vector<string> restore_ip_addresses(const string& s) {
    vector<string> result, parts;
    function<void(int)> backtrack = [&](int i) {
        if (parts.size() == 4) { if (i == static_cast<int>(s.size())) {
            string ip; for (const auto& p : parts) { if (!ip.empty()) ip += '.'; ip += p; } result.push_back(ip);
        } return; }
        int remaining = static_cast<int>(s.size()) - i, slots = 4 - static_cast<int>(parts.size());
        if (remaining < slots || remaining > 3 * slots) return;
        for (int length = 1; length <= 3 && i + length <= static_cast<int>(s.size()); ++length) {
            string part = s.substr(i, length);
            if (length > 1 && part[0] == '0') break;
            if (stoi(part) > 255) continue;
            parts.push_back(part); backtrack(i + length); parts.pop_back();
        }
    };
    backtrack(0); return result;
}

// ============================================================
// GRID BACKTRACKING
// ============================================================
bool word_search(vector<vector<char>>& board, const string& word) {
    int rows = static_cast<int>(board.size()), cols = rows ? static_cast<int>(board[0].size()) : 0;
    function<bool(int, int, int)> dfs = [&](int r, int c, int i) {
        if (i == static_cast<int>(word.size())) return true;
        if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] != word[i]) return false;
        char original = board[r][c]; board[r][c] = '#';
        bool found = dfs(r + 1, c, i + 1) || dfs(r - 1, c, i + 1) || dfs(r, c + 1, i + 1) || dfs(r, c - 1, i + 1);
        board[r][c] = original; return found;
    };
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (dfs(r, c, 0)) return true;
    return false;
}

vector<string> rat_in_maze(const vector<vector<int>>& maze) {
    int n = static_cast<int>(maze.size());
    if (!n || maze[0][0] == 0) return {};
    vector<string> result; vector<vector<bool>> visited(n, vector<bool>(n, false)); string path;
    const vector<tuple<int,int,char>> directions = {{1,0,'D'}, {0,-1,'L'}, {0,1,'R'}, {-1,0,'U'}};
    function<void(int,int)> backtrack = [&](int r, int c) {
        if (r == n - 1 && c == n - 1) { result.push_back(path); return; }
        visited[r][c] = true;
        for (auto [dr, dc, move] : directions) {
            int nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && maze[nr][nc] == 1 && !visited[nr][nc]) {
                path.push_back(move); backtrack(nr, nc); path.pop_back();
            }
        }
        visited[r][c] = false;
    };
    backtrack(0, 0); return result;
}

// ============================================================
// N-QUEENS
// ============================================================
vector<vector<string>> solve_n_queens(int n) {
    vector<vector<string>> result; vector<string> board(n, string(n, '.'));
    unordered_set<int> columns, diagonals, anti_diagonals;
    function<void(int)> backtrack = [&](int row) {
        if (row == n) { result.push_back(board); return; }
        for (int col = 0; col < n; ++col) {
            int d = row - col, ad = row + col;
            if (columns.count(col) || diagonals.count(d) || anti_diagonals.count(ad)) continue;
            board[row][col] = 'Q'; columns.insert(col); diagonals.insert(d); anti_diagonals.insert(ad);
            backtrack(row + 1);
            board[row][col] = '.'; columns.erase(col); diagonals.erase(d); anti_diagonals.erase(ad);
        }
    };
    backtrack(0); return result;
}

long long count_n_queens(int n) {
    unordered_set<int> columns, diagonals, anti_diagonals;
    function<long long(int)> backtrack = [&](int row) -> long long {
        if (row == n) return 1;
        long long count = 0;
        for (int col = 0; col < n; ++col) {
            int d = row - col, ad = row + col;
            if (columns.count(col) || diagonals.count(d) || anti_diagonals.count(ad)) continue;
            columns.insert(col); diagonals.insert(d); anti_diagonals.insert(ad);
            count += backtrack(row + 1);
            columns.erase(col); diagonals.erase(d); anti_diagonals.erase(ad);
        }
        return count;
    };
    return backtrack(0);
}

// ============================================================
// SUDOKU — mutates a 9x9 board in-place; empty cells are '.'
// ============================================================
bool solve_sudoku(vector<vector<char>>& board) {
    vector<unordered_set<char>> rows(9), cols(9), boxes(9); vector<pair<int,int>> empty;
    for (int r = 0; r < 9; ++r) for (int c = 0; c < 9; ++c) {
        char value = board[r][c];
        if (value == '.') empty.emplace_back(r, c);
        else { int b = (r / 3) * 3 + c / 3; rows[r].insert(value); cols[c].insert(value); boxes[b].insert(value); }
    }
    function<bool(int)> backtrack = [&](int index) {
        if (index == static_cast<int>(empty.size())) return true;
        auto [r, c] = empty[index]; int b = (r / 3) * 3 + c / 3;
        for (char digit = '1'; digit <= '9'; ++digit) {
            if (rows[r].count(digit) || cols[c].count(digit) || boxes[b].count(digit)) continue;
            board[r][c] = digit; rows[r].insert(digit); cols[c].insert(digit); boxes[b].insert(digit);
            if (backtrack(index + 1)) return true;
            board[r][c] = '.'; rows[r].erase(digit); cols[c].erase(digit); boxes[b].erase(digit);
        }
        return false;
    };
    return backtrack(0);
}

// ============================================================
// GRAPH COLORING
// ============================================================
vector<int> graph_coloring(const vector<vector<int>>& graph, int m) {
    int n = static_cast<int>(graph.size()); vector<int> colors(n, 0);
    auto valid = [&](int node, int color) {
        for (int neighbor = 0; neighbor < n; ++neighbor)
            if (graph[node][neighbor] && colors[neighbor] == color) return false;
        return true;
    };
    function<bool(int)> backtrack = [&](int node) {
        if (node == n) return true;
        for (int color = 1; color <= m; ++color) if (valid(node, color)) {
            colors[node] = color;
            if (backtrack(node + 1)) return true;
            colors[node] = 0;
        }
        return false;
    };
    return backtrack(0) ? colors : vector<int>{};
}

// ============================================================
// PARTITION / CONSTRAINT BACKTRACKING
// ============================================================
bool can_partition_k_subsets(vector<int> nums, int k) {
    long long total = accumulate(nums.begin(), nums.end(), 0LL);
    if (k <= 0 || k > static_cast<int>(nums.size()) || total % k != 0) return false;
    long long target = total / k;
    sort(nums.rbegin(), nums.rend());
    if (!nums.empty() && nums[0] > target) return false;
    vector<long long> buckets(k, 0);
    function<bool(int)> backtrack = [&](int i) {
        if (i == static_cast<int>(nums.size())) return true;
        int value = nums[i];
        for (int bucket = 0; bucket < k; ++bucket) {
            if (buckets[bucket] + value > target) continue;
            if (bucket > 0 && buckets[bucket] == buckets[bucket - 1]) continue; // symmetry pruning
            buckets[bucket] += value;
            if (backtrack(i + 1)) return true;
            buckets[bucket] -= value;
            if (buckets[bucket] == 0) break;
        }
        return false;
    };
    return backtrack(0);
}

// ============================================================
// BINARY STRING GENERATION
// ============================================================
vector<string> binary_strings(int n) {
    vector<string> result; string path;
    function<void()> backtrack = [&]() {
        if (static_cast<int>(path.size()) == n) { result.push_back(path); return; }
        for (char bit : string("01")) { path.push_back(bit); backtrack(); path.pop_back(); }
    };
    backtrack(); return result;
}

vector<string> binary_strings_no_consecutive_ones(int n) {
    vector<string> result; string path;
    function<void(int)> backtrack = [&](int previous) {
        if (static_cast<int>(path.size()) == n) { result.push_back(path); return; }
        path.push_back('0'); backtrack(0); path.pop_back();
        if (previous == 0) { path.push_back('1'); backtrack(1); path.pop_back(); }
    };
    backtrack(0); return result;
}

// ============================================================
// RECURSIVE SUBSET / TARGET PROBLEMS
// ============================================================
long long count_subsets_with_sum(const vector<int>& nums, int target) {
    function<long long(int, int)> solve = [&](int i, int remaining) -> long long {
        if (i == static_cast<int>(nums.size())) return remaining == 0;
        long long count = solve(i + 1, remaining);
        if (nums[i] <= remaining) count += solve(i + 1, remaining - nums[i]);
        return count;
    };
    return solve(0, target); // assumes non-negative values, as in the source version
}

long long target_sum_ways_naive(const vector<int>& nums, int target) {
    function<long long(int, long long)> solve = [&](int i, long long total) -> long long {
        if (i == static_cast<int>(nums.size())) return total == target;
        return solve(i + 1, total + nums[i]) + solve(i + 1, total - nums[i]);
    };
    return solve(0, 0);
}

// ============================================================
// GENERIC TEMPLATES (illustrative; intentionally not executable)
// ============================================================
/*
Recursion template:
    ReturnType solve(State state) {
        if (base_case) return answer;
        State smaller_state = make_smaller(state);
        auto result = solve(smaller_state);
        return combine(state, result);
    }

Backtracking template:
    void backtrack(State state) {
        if (complete) { record_answer(); return; }
        for (Choice choice : choices) {
            if (invalid(choice)) continue;
            choose(choice);
            backtrack(new_state);
            undo(choice);
        }
    }

Core idea: CHOOSE -> EXPLORE -> UNDO
Pruning: sorted candidates, duplicate skipping, remaining-sum checks,
constraint sets, symmetry breaking, early termination.
*/

// ============================================================
// PATTERN CHEAT SHEET
// ============================================================
/*
RECURSION
- Factorial: f(n) = n * f(n-1)
- Binary Search: eliminate half -> O(log n)
- Merge Sort: split + solve halves + merge -> O(n log n)
- Fibonacci: overlapping subproblems -> memoization / DP
- Tree: solve left + solve right + combine

BACKTRACKING
- Subsets: choose / don't choose; O(2^n) outputs
- Permutations: choose unused element; O(n!)
- Combinations: maintain start index; recurse with i+1
- Reusable candidates: recurse with i
- No reuse: recurse with i+1
- Duplicates: sort; skip when i > start && nums[i] == nums[i-1]
- Grid: mark -> explore -> unmark
- Constraints: choose -> validate -> recurse -> undo
- N-Queens: columns, row-col diagonals, row+col diagonals
- Sudoku: row set, column set, 3x3 box set

Interview questions: What is the state? Base case? Choices? Invalid choices?
What changes after choosing? What must be undone? Can we prune or memoize?
Recursion solves smaller problems; backtracking tries choices, explores, then undoes.
Memoize when paths can reach the same state. Output size can impose a lower bound.
*/

// ============================================================
// TEST SUITE
// ============================================================
void run_revision_tests() {
    assert(factorial(5) == 120); assert(fast_power(2, 10) == 1024);
    assert(fibonacci(10) == 55); assert(fibonacci_memo(30) == 832040);
    assert(sum_n(5) == 15); assert(digit_sum(12345) == 15); assert(count_digits(12345) == 5);
    assert(gcd_recursive(48, 18) == 6); assert(reverse_string("hello") == "olleh"); assert(is_palindrome("racecar"));
    vector<int> nums{1, 2, 2, 5};
    assert(recursive_array_sum(nums) == 10); assert(recursive_max(nums) == 5); assert(is_sorted_recursive(nums));
    assert(first_occurrence(nums, 2) == 1); assert(last_occurrence(nums, 2) == 2); assert(binary_search_recursive(nums, 5) == 3);
    assert(merge_sort({5,1,4,2,3}) == vector<int>({1,2,3,4,5}));
    assert(quick_sort({5,1,4,2,3}) == vector<int>({1,2,3,4,5}));
    ListNode* head = new ListNode(1, new ListNode(2, new ListNode(3)));
    head = reverse_linked_list_recursive(head); assert(linked_list_to_vector(head) == vector<int>({3,2,1}));
    while (head) { ListNode* next = head->next; delete head; head = next; }
    TreeNode* root = new TreeNode(1); root->left = new TreeNode(2); root->right = new TreeNode(3);
    root->left->left = new TreeNode(4); root->left->right = new TreeNode(5);
    assert(preorder(root) == vector<int>({1,2,4,5,3})); assert(inorder(root) == vector<int>({4,2,5,1,3}));
    assert(postorder(root) == vector<int>({4,5,2,3,1})); assert(tree_height(root) == 3); assert(tree_diameter(root) == 3);
    assert(climbing_stairs(5) == 8); assert(house_robber_recursive({2,7,9,3,1}) == 12);
    assert(target_sum_ways({1,1,1,1,1}, 3) == 5);
    assert(subsets({1,2,3}).size() == 8); assert(subsets_with_duplicates({1,2,2}).size() == 6);
    assert(permutations({1,2,3}).size() == 6); assert(permutations_swap({1,2,3}).size() == 6);
    assert(permutations_with_duplicates({1,1,2}).size() == 3);
    assert(combination_sum({2,3,6,7}, 7) == vector<vector<int>>({{2,2,3},{7}}));
    assert(combination_sum_ii({10,1,2,7,6,1,5}, 8) == vector<vector<int>>({{1,1,6},{1,2,5},{1,7},{2,6}}));
    assert(combination_sum_iii(3, 7) == vector<vector<int>>({{1,2,4}}));
    assert(letter_combinations("23").size() == 9);
    assert(generate_parentheses(3) == vector<string>({"((()))","(()())","(())()","()(())","()()()"}));
    assert(palindrome_partition("aab") == vector<vector<string>>({{"a","a","b"},{"aa","b"}}));
    assert(solve_n_queens(4).size() == 2); assert(count_n_queens(4) == 2);
    vector<vector<char>> board{{'A','B','C','E'},{'S','F','C','S'},{'A','D','E','E'}};
    assert(word_search(board, "ABCCED"));
    vector<vector<int>> maze{{1,0,0,0},{1,1,0,1},{0,1,0,0},{1,1,1,1}};
    auto paths = rat_in_maze(maze); assert(find(paths.begin(), paths.end(), "DRDDRR") != paths.end());
    assert(binary_strings(2) == vector<string>({"00","01","10","11"}));
    assert(binary_strings_no_consecutive_ones(3) == vector<string>({"000","001","010","100","101"}));
    auto cases = letter_case_permutation("a1b"); sort(cases.begin(), cases.end());
    vector<string> expected_cases{"a1b","a1B","A1b","A1B"}; sort(expected_cases.begin(), expected_cases.end()); assert(cases == expected_cases);
    auto ips = restore_ip_addresses("25525511135"); sort(ips.begin(), ips.end());
    vector<string> expected_ips{"255.255.11.135","255.255.111.35"}; sort(expected_ips.begin(), expected_ips.end()); assert(ips == expected_ips);
    assert(combinations(4, 2) == vector<vector<int>>({{1,2},{1,3},{1,4},{2,3},{2,4},{3,4}}));
    assert(can_partition_k_subsets({4,3,2,3,5,2,1}, 4));
    cout << "All Recursion + Backtracking revision tests passed! \n";
}

int main() {
    cout << string(70, '=') << '\n';
    cout << "RECURSION + BACKTRACKING — COMPLETE REVISION (C++17)\n";
    cout << string(70, '=') << '\n';
    cout << "Run run_revision_tests() to verify all implementations.\n";
    run_revision_tests();
}

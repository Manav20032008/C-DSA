/*
ARRAYS — COMPLETE DSA REVISION (C++17)
Placement-focused revision library converted from the supplied Python codebook.

Topics:
- Basic operations, prefix sums, difference arrays
- Two pointers, sliding window, Kadane, hashing
- Rotation, merging, intervals, binary search
- Binary search on answer, sorting, frequency/bucket patterns
- Greedy, matrices, subarray/subsequence patterns
- Monotonic stacks, heaps, 2D prefix sums
- Pattern-recognition and complexity cheat sheets

Compile as a translation unit:
    g++ -std=c++17 -O2 -Wall -Wextra arrays_complete_revision.cpp
*/

#include <algorithm>
#include <cassert>
#include <climits>
#include <cmath>
#include <functional>
#include <tuple>
#include <iostream>
#include <numeric>
#include <queue>
#include <stack>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

using namespace std;
using ll = long long;
using pii = pair<int, int>;
using vi = vector<int>;
using vll = vector<ll>;
using vvi = vector<vi>;
using vvll = vector<vll>;

// ============================================================
// BASIC ARRAY OPERATIONS
// ============================================================

vi traverse(const vi& arr) { return arr; }

vi insert_at(vi arr, int index, int value) {
    arr.insert(arr.begin() + index, value);
    return arr;
}

vi delete_at(vi arr, int index) {
    arr.erase(arr.begin() + index);
    return arr;
}

int linear_search(const vi& arr, int target) {
    for (int i = 0; i < (int)arr.size(); ++i)
        if (arr[i] == target) return i;
    return -1;
}

vi reverse_array(vi arr) {
    reverse(arr.begin(), arr.end());
    return arr;
}

vi reverse_array_in_place(vi arr) {
    int left = 0, right = (int)arr.size() - 1;
    while (left < right) swap(arr[left++], arr[right--]);
    return arr;
}

// ============================================================
// PREFIX SUM
// ============================================================

vll prefix_sum(const vi& arr) {
    vll prefix(arr.size() + 1, 0);
    for (size_t i = 0; i < arr.size(); ++i)
        prefix[i + 1] = prefix[i] + arr[i];
    return prefix;
}

// Inclusive range sum [left, right].
ll range_sum(const vi& arr, int left, int right) {
    auto prefix = prefix_sum(arr);
    return prefix[right + 1] - prefix[left];
}

ll subarray_sum_equals_k(const vi& arr, ll k) {
    unordered_map<ll, ll> prefix_count{{0, 1}};
    ll current_sum = 0, count = 0;
    for (int value : arr) {
        current_sum += value;
        auto it = prefix_count.find(current_sum - k);
        if (it != prefix_count.end()) count += it->second;
        ++prefix_count[current_sum];
    }
    return count;
}

// ============================================================
// DIFFERENCE ARRAY
// ============================================================

// updates = { {left, right, value}, ... }; inclusive endpoints.
vi range_increment(int n, const vector<tuple<int, int, int>>& updates) {
    vi diff(n + 1, 0);
    for (auto [left, right, value] : updates) {
        diff[left] += value;
        if (right + 1 < (int)diff.size()) diff[right + 1] -= value;
    }
    vi result(n, 0);
    int current = 0;
    for (int i = 0; i < n; ++i) {
        current += diff[i];
        result[i] = current;
    }
    return result;
}

// ============================================================
// TWO POINTERS
// ============================================================

vi two_sum_sorted(const vi& arr, int target) {
    int left = 0, right = (int)arr.size() - 1;
    while (left < right) {
        ll total = (ll)arr[left] + arr[right];
        if (total == target) return {left, right};
        if (total < target) ++left;
        else --right;
    }
    return {};
}

vi remove_duplicates_sorted(const vi& arr) {
    vi result;
    for (int value : arr)
        if (result.empty() || value != result.back()) result.push_back(value);
    return result;
}

vi move_zeroes(vi arr) {
    int write = 0;
    for (int value : arr)
        if (value != 0) arr[write++] = value;
    while (write < (int)arr.size()) arr[write++] = 0;
    return arr;
}

bool is_palindrome_array(const vi& arr) {
    int left = 0, right = (int)arr.size() - 1;
    while (left < right)
        if (arr[left++] != arr[right--]) return false;
    return true;
}

ll container_with_most_water(const vi& height) {
    int left = 0, right = (int)height.size() - 1;
    ll best = 0;
    while (left < right) {
        ll area = (ll)(right - left) * min(height[left], height[right]);
        best = max(best, area);
        if (height[left] < height[right]) ++left;
        else --right;
    }
    return best;
}

vvi three_sum(vi nums) {
    sort(nums.begin(), nums.end());
    vvi result;
    for (int i = 0; i + 2 < (int)nums.size(); ++i) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int left = i + 1, right = (int)nums.size() - 1;
        while (left < right) {
            ll total = (ll)nums[i] + nums[left] + nums[right];
            if (total == 0) {
                result.push_back({nums[i], nums[left], nums[right]});
                ++left; --right;
                while (left < right && nums[left] == nums[left - 1]) ++left;
                while (left < right && nums[right] == nums[right + 1]) --right;
            } else if (total < 0) ++left;
            else --right;
        }
    }
    return result;
}

// ============================================================
// SLIDING WINDOW
// ============================================================

ll max_sum_subarray_fixed_k(const vi& arr, int k) {
    if (k <= 0 || k > (int)arr.size()) return LLONG_MIN;
    ll window_sum = accumulate(arr.begin(), arr.begin() + k, 0LL);
    ll best = window_sum;
    for (int right = k; right < (int)arr.size(); ++right) {
        window_sum += arr[right] - arr[right - k];
        best = max(best, window_sum);
    }
    return best;
}

tuple<ll, int, int> max_sum_subarray_fixed_k_indices(const vi& arr, int k) {
    if (k <= 0 || k > (int)arr.size()) return {LLONG_MIN, -1, -1};
    ll window_sum = accumulate(arr.begin(), arr.begin() + k, 0LL);
    ll best = window_sum;
    int best_left = 0;
    for (int right = k; right < (int)arr.size(); ++right) {
        window_sum += arr[right] - arr[right - k];
        if (window_sum > best) {
            best = window_sum;
            best_left = right - k + 1;
        }
    }
    return {best, best_left, best_left + k - 1};
}

// Assumes all array values are non-negative.
int longest_subarray_sum_at_most_k_positive(const vi& arr, ll k) {
    int left = 0, best = 0;
    ll current = 0;
    for (int right = 0; right < (int)arr.size(); ++right) {
        current += arr[right];
        while (current > k && left <= right) current -= arr[left++];
        best = max(best, right - left + 1);
    }
    return best;
}

// Assumes positive/non-negative elements for the usual sliding-window method.
int min_subarray_len(ll target, const vi& nums) {
    int left = 0, best = INT_MAX;
    ll current = 0;
    for (int right = 0; right < (int)nums.size(); ++right) {
        current += nums[right];
        while (current >= target) {
            best = min(best, right - left + 1);
            current -= nums[left++];
        }
    }
    return best == INT_MAX ? 0 : best;
}

int longest_substring_without_repeating(const string& s) {
    int left = 0, best = 0;
    unordered_map<char, int> last_seen;
    for (int right = 0; right < (int)s.size(); ++right) {
        char c = s[right];
        if (last_seen.count(c) && last_seen[c] >= left)
            left = last_seen[c] + 1;
        last_seen[c] = right;
        best = max(best, right - left + 1);
    }
    return best;
}

// ============================================================
// KADANE'S ALGORITHM
// ============================================================

ll max_subarray_sum(const vi& nums) {
    if (nums.empty()) return 0;
    ll current = nums[0], best = nums[0];
    for (int i = 1; i < (int)nums.size(); ++i) {
        current = max((ll)nums[i], current + nums[i]);
        best = max(best, current);
    }
    return best;
}

tuple<ll, int, int> max_subarray_with_indices(const vi& nums) {
    if (nums.empty()) return {0, -1, -1};
    ll current = nums[0], best = nums[0];
    int current_start = 0, best_start = 0, best_end = 0;
    for (int i = 1; i < (int)nums.size(); ++i) {
        if (nums[i] > current + nums[i]) {
            current = nums[i];
            current_start = i;
        } else current += nums[i];

        if (current > best) {
            best = current;
            best_start = current_start;
            best_end = i;
        }
    }
    return {best, best_start, best_end};
}

ll max_circular_subarray_sum(const vi& nums) {
    if (nums.empty()) return 0;
    ll total = accumulate(nums.begin(), nums.end(), 0LL);
    ll normal = max_subarray_sum(nums);
    ll min_current = nums[0], min_best = nums[0];
    for (int i = 1; i < (int)nums.size(); ++i) {
        min_current = min((ll)nums[i], min_current + nums[i]);
        min_best = min(min_best, min_current);
    }
    if (normal < 0) return normal;
    return max(normal, total - min_best);
}

// ============================================================
// HASHING ARRAY PATTERNS
// ============================================================

vi two_sum(const vi& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int complement = target - nums[i];
        if (seen.count(complement)) return {seen[complement], i};
        seen[nums[i]] = i;
    }
    return {};
}

int longest_consecutive_sequence(const vi& nums) {
    unordered_set<int> values(nums.begin(), nums.end());
    int best = 0;
    for (int value : values) {
        if (!values.count(value - 1)) {
            int current = value;
            while (values.count(current + 1)) ++current;
            best = max(best, current - value + 1);
        }
    }
    return best;
}

// Boyer-Moore; assumes a majority element exists.
int majority_element(const vi& nums) {
    int candidate = 0, count = 0;
    for (int value : nums) {
        if (count == 0) candidate = value;
        count += (value == candidate) ? 1 : -1;
    }
    return candidate;
}

vi majority_elements_n_by_3(const vi& nums) {
    int candidate1 = 0, candidate2 = 1, count1 = 0, count2 = 0;
    for (int value : nums) {
        if (value == candidate1) ++count1;
        else if (value == candidate2) ++count2;
        else if (count1 == 0) candidate1 = value, count1 = 1;
        else if (count2 == 0) candidate2 = value, count2 = 1;
        else --count1, --count2;
    }
    vi result;
    int actual1 = 0, actual2 = 0;
    for (int value : nums) {
        if (value == candidate1) ++actual1;
        if (value == candidate2) ++actual2;
    }
    if (actual1 > (int)nums.size() / 3) result.push_back(candidate1);
    if (candidate2 != candidate1 && actual2 > (int)nums.size() / 3)
        result.push_back(candidate2);
    return result;
}

int longest_zero_sum_subarray(const vi& nums) {
    unordered_map<ll, int> first_index{{0, -1}};
    ll current_sum = 0;
    int best = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
        current_sum += nums[i];
        if (first_index.count(current_sum))
            best = max(best, i - first_index[current_sum]);
        else first_index[current_sum] = i;
    }
    return best;
}

// ============================================================
// ROTATION
// ============================================================

// Right rotate by k positions.
vi rotate_array(vi nums, int k) {
    if (nums.empty()) return {};
    k %= (int)nums.size();
    reverse(nums.begin(), nums.end());
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
    return nums;
}

vi rotate_array_simple(const vi& nums, int k) {
    if (nums.empty()) return {};
    int n = (int)nums.size();
    k %= n;
    vi result;
    result.insert(result.end(), nums.end() - k, nums.end());
    result.insert(result.end(), nums.begin(), nums.end() - k);
    return result;
}

// ============================================================
// MERGING AND INTERVALS
// ============================================================

vi merge_sorted_arrays(const vi& a, const vi& b) {
    vi result;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] <= b[j]) result.push_back(a[i++]);
        else result.push_back(b[j++]);
    }
    result.insert(result.end(), a.begin() + i, a.end());
    result.insert(result.end(), b.begin() + j, b.end());
    return result;
}

vvi merge_intervals(vvi intervals) {
    if (intervals.empty()) return {};
    sort(intervals.begin(), intervals.end());
    vvi result{intervals[0]};
    for (int i = 1; i < (int)intervals.size(); ++i) {
        if (intervals[i][0] <= result.back()[1])
            result.back()[1] = max(result.back()[1], intervals[i][1]);
        else result.push_back(intervals[i]);
    }
    return result;
}

vvi insert_interval(const vvi& intervals, vi new_interval) {
    vvi result;
    int i = 0, n = (int)intervals.size();
    while (i < n && intervals[i][1] < new_interval[0])
        result.push_back(intervals[i++]);
    while (i < n && intervals[i][0] <= new_interval[1]) {
        new_interval[0] = min(new_interval[0], intervals[i][0]);
        new_interval[1] = max(new_interval[1], intervals[i][1]);
        ++i;
    }
    result.push_back(new_interval);
    result.insert(result.end(), intervals.begin() + i, intervals.end());
    return result;
}

vvi interval_intersection(const vvi& a, const vvi& b) {
    int i = 0, j = 0;
    vvi result;
    while (i < (int)a.size() && j < (int)b.size()) {
        int start = max(a[i][0], b[j][0]);
        int end = min(a[i][1], b[j][1]);
        if (start <= end) result.push_back({start, end});
        if (a[i][1] < b[j][1]) ++i;
        else ++j;
    }
    return result;
}

// ============================================================
// BINARY SEARCH
// ============================================================

int binary_search(const vi& arr, int target) {
    int left = 0, right = (int)arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int lower_bound_index(const vi& arr, int target) {
    return (int)(lower_bound(arr.begin(), arr.end(), target) - arr.begin());
}

int upper_bound_index(const vi& arr, int target) {
    return (int)(upper_bound(arr.begin(), arr.end(), target) - arr.begin());
}

vi search_range(const vi& arr, int target) {
    int left = lower_bound_index(arr, target);
    if (left == (int)arr.size() || arr[left] != target) return {-1, -1};
    return {left, upper_bound_index(arr, target) - 1};
}

int search_rotated_sorted_array(const vi& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[left] <= nums[mid]) {
            if (nums[left] <= target && target < nums[mid]) right = mid - 1;
            else left = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[right]) left = mid + 1;
            else right = mid - 1;
        }
    }
    return -1;
}

int find_min_rotated_sorted_array(const vi& nums) {
    int left = 0, right = (int)nums.size() - 1;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] > nums[right]) left = mid + 1;
        else right = mid;
    }
    return nums[left];
}

int find_peak_element(const vi& nums) {
    int left = 0, right = (int)nums.size() - 1;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] < nums[mid + 1]) left = mid + 1;
        else right = mid;
    }
    return left;
}

// ============================================================
// BINARY SEARCH ON ANSWER
// ============================================================

int integer_square_root(int x) {
    if (x < 2) return x;
    int left = 1, right = x / 2, answer = 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (mid <= x / mid) answer = mid, left = mid + 1;
        else right = mid - 1;
    }
    return answer;
}

int koko_eating_bananas(const vi& piles, int h) {
    int left = 1, right = *max_element(piles.begin(), piles.end());
    while (left < right) {
        int speed = left + (right - left) / 2;
        ll hours = 0;
        for (int pile : piles) hours += (pile + speed - 1LL) / speed;
        if (hours <= h) right = speed;
        else left = speed + 1;
    }
    return left;
}

int ship_within_days(const vi& weights, int days) {
    int left = *max_element(weights.begin(), weights.end());
    ll right = accumulate(weights.begin(), weights.end(), 0LL);
    auto can_ship = [&](ll capacity) {
        int used_days = 1;
        ll current = 0;
        for (int weight : weights) {
            if (current + weight > capacity) {
                ++used_days;
                current = 0;
            }
            current += weight;
        }
        return used_days <= days;
    };
    while (left < right) {
        ll capacity = left + (right - left) / 2;
        if (can_ship(capacity)) right = capacity;
        else left = (int)capacity + 1;
    }
    return left;
}

// ============================================================
// SORTING
// ============================================================

// The supplied Python heap_sort implementation delegates to sorted().
vi heap_sort(vi arr) {
    sort(arr.begin(), arr.end());
    return arr;
}

// ============================================================
// SPECIAL SORTING PATTERNS
// ============================================================

vi sort_colors(vi nums) {
    int low = 0, mid = 0, high = (int)nums.size() - 1;
    while (mid <= high) {
        if (nums[mid] == 0) swap(nums[low++], nums[mid++]);
        else if (nums[mid] == 1) ++mid;
        else swap(nums[mid], nums[high--]);
    }
    return nums;
}

ll count_inversions(vi nums) {
    vi temp(nums.size());
    function<ll(int, int)> merge_sort_count = [&](int left, int right) -> ll {
        if (right - left <= 1) return 0;
        int mid = left + (right - left) / 2;
        ll count = merge_sort_count(left, mid) + merge_sort_count(mid, right);
        int i = left, j = mid, k = left;
        while (i < mid && j < right) {
            if (nums[i] <= nums[j]) temp[k++] = nums[i++];
            else {
                temp[k++] = nums[j++];
                count += mid - i;
            }
        }
        while (i < mid) temp[k++] = nums[i++];
        while (j < right) temp[k++] = nums[j++];
        for (int p = left; p < right; ++p) nums[p] = temp[p];
        return count;
    };
    return merge_sort_count(0, (int)nums.size());
}

// ============================================================
// FREQUENCY / BUCKET PATTERNS
// ============================================================

vi top_k_frequent(const vi& nums, int k) {
    unordered_map<int, int> frequency;
    for (int value : nums) ++frequency[value];
    vector<vi> buckets(nums.size() + 1);
    for (auto [value, count] : frequency) buckets[count].push_back(value);
    vi result;
    for (int count = (int)buckets.size() - 1; count > 0; --count) {
        for (int value : buckets[count]) {
            result.push_back(value);
            if ((int)result.size() == k) return result;
        }
    }
    return result;
}

vll product_except_self(const vi& nums) {
    vll result(nums.size(), 1);
    ll prefix = 1;
    for (int i = 0; i < (int)nums.size(); ++i) {
        result[i] = prefix;
        prefix *= nums[i];
    }
    ll suffix = 1;
    for (int i = (int)nums.size() - 1; i >= 0; --i) {
        result[i] *= suffix;
        suffix *= nums[i];
    }
    return result;
}

// ============================================================
// GREEDY ARRAY PATTERNS
// ============================================================

bool can_jump(const vi& nums) {
    int farthest = 0;
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (i > farthest) return false;
        farthest = max(farthest, i + nums[i]);
    }
    return true;
}

int jump_game_min_jumps(const vi& nums) {
    if (nums.size() <= 1) return 0;
    int jumps = 0, current_end = 0, farthest = 0;
    for (int i = 0; i < (int)nums.size() - 1; ++i) {
        farthest = max(farthest, i + nums[i]);
        if (i == current_end) {
            ++jumps;
            current_end = farthest;
        }
    }
    return jumps;
}

int gas_station(const vi& gas, const vi& cost) {
    if (accumulate(gas.begin(), gas.end(), 0LL) <
        accumulate(cost.begin(), cost.end(), 0LL)) return -1;
    int start = 0;
    ll tank = 0;
    for (int i = 0; i < (int)gas.size(); ++i) {
        tank += gas[i] - cost[i];
        if (tank < 0) start = i + 1, tank = 0;
    }
    return start;
}

// ============================================================
// MATRIX / 2D ARRAYS
// ============================================================

vvi transpose_matrix(const vvi& matrix) {
    if (matrix.empty()) return {};
    vvi result(matrix[0].size(), vi(matrix.size()));
    for (int r = 0; r < (int)matrix.size(); ++r)
        for (int c = 0; c < (int)matrix[0].size(); ++c)
            result[c][r] = matrix[r][c];
    return result;
}

// Clockwise 90-degree rotation; requires a square matrix.
vvi rotate_matrix_90(vvi matrix) {
    if (matrix.empty()) return {};
    int n = (int)matrix.size();
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            swap(matrix[i][j], matrix[j][i]);
    for (auto& row : matrix) reverse(row.begin(), row.end());
    return matrix;
}

vi spiral_order(const vvi& matrix) {
    if (matrix.empty() || matrix[0].empty()) return {};
    int top = 0, bottom = (int)matrix.size() - 1;
    int left = 0, right = (int)matrix[0].size() - 1;
    vi result;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; ++c) result.push_back(matrix[top][c]);
        ++top;
        for (int r = top; r <= bottom; ++r) result.push_back(matrix[r][right]);
        --right;
        if (top <= bottom) {
            for (int c = right; c >= left; --c) result.push_back(matrix[bottom][c]);
            --bottom;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; --r) result.push_back(matrix[r][left]);
            ++left;
        }
    }
    return result;
}

// Rows and columns sorted increasingly.
bool search_sorted_matrix(const vvi& matrix, int target) {
    if (matrix.empty() || matrix[0].empty()) return false;
    int row = 0, col = (int)matrix[0].size() - 1;
    while (row < (int)matrix.size() && col >= 0) {
        if (matrix[row][col] == target) return true;
        if (matrix[row][col] > target) --col;
        else ++row;
    }
    return false;
}

// ============================================================
// SUBARRAY / SUBSEQUENCE PATTERNS
// ============================================================

ll max_product_subarray(const vi& nums) {
    if (nums.empty()) return 0;
    ll current_max = nums[0], current_min = nums[0], result = nums[0];
    for (int i = 1; i < (int)nums.size(); ++i) {
        if (nums[i] < 0) swap(current_max, current_min);
        current_max = max((ll)nums[i], current_max * nums[i]);
        current_min = min((ll)nums[i], current_min * nums[i]);
        result = max(result, current_max);
    }
    return result;
}

// O(n log n) LIS length; strict increasing subsequence.
int longest_increasing_subsequence(const vi& nums) {
    vi tails;
    for (int value : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), value);
        if (it == tails.end()) tails.push_back(value);
        else *it = value;
    }
    return (int)tails.size();
}

int maximum_length_subarray_positive(const vi& nums) {
    int best = 0, current = 0;
    for (int value : nums) {
        if (value > 0) best = max(best, ++current);
        else current = 0;
    }
    return best;
}

// ============================================================
// MONOTONIC STACK ARRAY PATTERNS
// ============================================================

vi next_greater_element(const vi& nums) {
    vi result(nums.size(), -1);
    stack<int> st;
    for (int i = (int)nums.size() - 1; i >= 0; --i) {
        while (!st.empty() && st.top() <= nums[i]) st.pop();
        if (!st.empty()) result[i] = st.top();
        st.push(nums[i]);
    }
    return result;
}

vi daily_temperatures(const vi& temperatures) {
    vi result(temperatures.size(), 0);
    stack<int> st;
    for (int i = 0; i < (int)temperatures.size(); ++i) {
        while (!st.empty() && temperatures[st.top()] < temperatures[i]) {
            int previous = st.top(); st.pop();
            result[previous] = i - previous;
        }
        st.push(i);
    }
    return result;
}

ll largest_rectangle_histogram(vi heights) {
    heights.push_back(0);
    stack<int> st;
    ll best = 0;
    for (int i = 0; i < (int)heights.size(); ++i) {
        while (!st.empty() && heights[st.top()] > heights[i]) {
            int h = heights[st.top()]; st.pop();
            int left = st.empty() ? -1 : st.top();
            ll width = i - left - 1;
            best = max(best, (ll)h * width);
        }
        st.push(i);
    }
    return best;
}

// ============================================================
// RANDOMIZED / SELECTION PATTERN
// ============================================================

int kth_largest_heap(const vi& nums, int k) {
    priority_queue<int, vi, greater<int>> heap;
    for (int value : nums) {
        heap.push(value);
        if ((int)heap.size() > k) heap.pop();
    }
    return heap.top();
}

// ============================================================
// 2D PREFIX SUM
// ============================================================

class NumMatrix {
private:
    vvll prefix;

public:
    explicit NumMatrix(const vvi& matrix) {
        if (matrix.empty() || matrix[0].empty()) {
            prefix = {{0}};
            return;
        }
        int rows = (int)matrix.size(), cols = (int)matrix[0].size();
        prefix.assign(rows + 1, vll(cols + 1, 0));
        for (int r = 0; r < rows; ++r)
            for (int c = 0; c < cols; ++c)
                prefix[r + 1][c + 1] = matrix[r][c]
                    + prefix[r][c + 1] + prefix[r + 1][c]
                    - prefix[r][c];
    }

    // Inclusive region [r1,c1] to [r2,c2].
    ll sum_region(int r1, int c1, int r2, int c2) const {
        const auto& p = prefix;
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1]
             - p[r2 + 1][c1] + p[r1][c1];
    }
};

/*
PATTERN RECOGNITION CHEAT SHEET
===============================

1. Direct traversal?                         -> Simple loop
2. Repeated range sums?                      -> Prefix sum
3. Repeated range updates?                   -> Difference array
4. Sorted array + pair relationship?         -> Two pointers
5. Contiguous subarray + fixed size?         -> Fixed sliding window
6. Contiguous subarray + dynamic condition?  -> Sliding window; check negatives
7. Maximum contiguous sum?                   -> Kadane
8. Pair sum?                                 -> Hash map; two pointers if sorted
9. Remove duplicates from sorted array?      -> Two pointers
10. Search sorted array?                     -> Binary search
11. Sorted array rotated?                     -> Modified binary search
12. Min possible max / max possible min?      -> Binary search on answer
13. Intervals overlap?                       -> Sort + merge / sweep
14. Need top K?                              -> Heap / bucket / sorting
15. Next/previous greater?                   -> Monotonic stack
16. Matrix boundary traversal?               -> Spiral / simulation
17. Grid row + column sorted?                -> Staircase search
18. O(1) extra-space rearrangement?           -> In-place / two pointers
19. Values 1..n, missing/repeated?            -> Cyclic sort / XOR / frequency
20. Longest consecutive values?              -> Hash set
21. Majority element?                         -> Boyer-Moore
22. Product except self?                      -> Prefix + suffix
23. Maximum product subarray?                -> Track current max + min
24. Reachability through jumps?              -> Greedy
25. Minimum jumps?                            -> Greedy level expansion
26. Minimum capacity to satisfy days?         -> Binary search on answer

COMPLEXITY CHEAT SHEET
======================

Traversal: O(n) time, O(1) auxiliary space
Prefix sum: O(n) build, O(1) query
Hash map lookup: O(1) average
Two pointers: usually O(n)
Sliding window: usually O(n)
Kadane: O(n) time, O(1) auxiliary space
Binary search: O(log n) time, O(1) auxiliary space
Merge sort: O(n log n) time, O(n) space
Quick sort: O(n log n) average, O(n^2) worst
Heap insert/remove: O(log n); peek O(1)
LIS: O(n log n)
Monotonic stack: usually O(n)
2D prefix sum: O(rows*cols) build, O(1) query

BINARY SEARCH ON ANSWER
======================

1. Define the answer space.
2. Pick a candidate answer.
3. Write a feasibility function.
4. Check whether the candidate works.
5. Use monotonicity to eliminate half the search space.

Examples: Koko Eating Bananas, Ship Packages Within D Days,
Split Array Largest Sum, Allocate Books, Aggressive Cows,
capacity / speed / distance problems.

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

FOUNDATION: traversal, search, insert/delete, reverse, in-place manipulation
PREFIX/RANGE: prefix sum, difference array, subarray sum, 2D prefix sum
TWO POINTERS: pair sum, remove duplicates, move zeroes, palindrome, container, 3Sum
SLIDING WINDOW: fixed, variable, longest valid, minimum valid, frequency-based
KADANE: maximum subarray, recover subarray, circular maximum, maximum product
HASHING: Two Sum, frequency map, longest consecutive, zero-sum, majority
BINARY SEARCH: basic, lower/upper bound, first/last, rotated, peak, answer search
SORTING: bubble, selection, insertion, merge, quick, heap, Dutch flag, inversions
INTERVALS: merge, insert, intersection, scheduling
GREEDY: Jump Game, minimum jumps, Gas Station
MATRIX: transpose, rotate, spiral, search, 2D prefix sum
ADVANCED: monotonic stack, top K, LIS, histogram, difference arrays

THE GOLDEN ARRAY QUESTIONS
==========================

Before coding, ask:
1. Is the array sorted?
2. Is the answer contiguous?
3. Is it a subarray or subsequence?
4. Is there a fixed or variable window?
5. Can I use two pointers?
6. Can prefix sums remove repeated work?
7. Can a hash map provide O(1) average lookup?
8. Is there monotonicity / can I binary-search the answer?
9. Is this asking for maximum/minimum?
10. Is there a greedy invariant?
11. Do I need to preserve order?
12. Can I modify the array in place?
13. Is a monotonic stack hiding in the problem?
14. Is this an interval or matrix problem?

Many unseen array problems become pattern-recognition exercises rather than
memorization exercises.
*/

#ifdef ARRAYS_REVISION_TEST
int main() {
    assert(traverse({1, 2, 3}) == vi({1, 2, 3}));
    assert(insert_at({1, 3}, 1, 2) == vi({1, 2, 3}));
    assert(delete_at({1, 2, 3}, 1) == vi({1, 3}));
    assert(linear_search({4, 7, 9}, 7) == 1);
    assert(reverse_array({1, 2, 3}) == vi({3, 2, 1}));
    assert(prefix_sum({1, 2, 3}) == vll({0, 1, 3, 6}));
    assert(range_sum({1, 2, 3, 4}, 1, 3) == 9);
    assert(subarray_sum_equals_k({1, 1, 1}, 2) == 2);
    assert(range_increment(5, {{1, 3, 2}, {2, 4, 3}}) == vi({0, 2, 5, 5, 3}));
    assert(two_sum_sorted({1, 2, 4, 7}, 6) == vi({1, 2}));
    assert(remove_duplicates_sorted({1, 1, 2, 2, 3}) == vi({1, 2, 3}));
    assert(move_zeroes({0, 1, 0, 3, 12}) == vi({1, 3, 12, 0, 0}));
    assert(is_palindrome_array({1, 2, 1}));
    assert(container_with_most_water({1, 8, 6, 2, 5, 4, 8, 3, 7}) == 49);
    assert(three_sum({-1, 0, 1, 2, -1, -4}) == vvi({{-1, -1, 2}, {-1, 0, 1}}));
    assert(max_sum_subarray_fixed_k({2, 1, 5, 1, 3, 2}, 3) == 9);
    assert(min_subarray_len(7, {2, 3, 1, 2, 4, 3}) == 2);
    assert(longest_substring_without_repeating("abcabcbb") == 3);
    assert(max_subarray_sum({-2, 1, -3, 4, -1, 2, 1, -5, 4}) == 6);
    assert(max_circular_subarray_sum({5, -3, 5}) == 10);
    assert(two_sum({2, 7, 11, 15}, 9) == vi({0, 1}));
    assert(longest_consecutive_sequence({100, 4, 200, 1, 3, 2}) == 4);
    assert(majority_element({2, 2, 1, 1, 1, 2, 2}) == 2);
    assert(longest_zero_sum_subarray({15, -2, 2, -8, 1, 7, 10, 23}) == 5);
    assert(rotate_array({1, 2, 3, 4, 5}, 2) == vi({4, 5, 1, 2, 3}));
    assert(merge_sorted_arrays({1, 3, 5}, {2, 4, 6}) == vi({1, 2, 3, 4, 5, 6}));
    assert(merge_intervals({{1, 3}, {2, 6}, {8, 10}, {9, 11}}) == vvi({{1, 6}, {8, 11}}));
    assert(insert_interval({{1, 3}, {6, 9}}, {2, 5}) == vvi({{1, 5}, {6, 9}}));
    assert(binary_search({1, 3, 5, 7}, 5) == 2);
    assert(lower_bound_index({1, 2, 2, 4}, 2) == 1);
    assert(upper_bound_index({1, 2, 2, 4}, 2) == 3);
    assert(search_range({5, 7, 7, 8, 8, 10}, 8) == vi({3, 4}));
    assert(search_rotated_sorted_array({4, 5, 6, 7, 0, 1, 2}, 0) == 4);
    assert(find_min_rotated_sorted_array({4, 5, 6, 7, 0, 1, 2}) == 0);
    assert(find_peak_element({1, 2, 3, 1}) == 2);
    assert(integer_square_root(17) == 4);
    assert(koko_eating_bananas({3, 6, 7, 11}, 8) == 4);
    assert(ship_within_days({1, 2, 3, 1, 1}, 4) == 3);
    assert(sort_colors({2, 0, 2, 1, 1, 0}) == vi({0, 0, 1, 1, 2, 2}));
    assert(count_inversions({1, 20, 6, 4, 5}) == 5);
    assert(product_except_self({1, 2, 3, 4}) == vll({24, 12, 8, 6}));
    assert(can_jump({2, 3, 1, 1, 4}));
    assert(!can_jump({3, 2, 1, 0, 4}));
    assert(jump_game_min_jumps({2, 3, 1, 1, 4}) == 2);
    assert(gas_station({1, 2, 3, 4, 5}, {3, 4, 5, 1, 2}) == 3);
    assert(transpose_matrix({{1, 2}, {3, 4}}) == vvi({{1, 3}, {2, 4}}));
    assert(rotate_matrix_90({{1, 2}, {3, 4}}) == vvi({{3, 1}, {4, 2}}));
    assert(spiral_order({{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}) == vi({1, 2, 3, 6, 9, 8, 7, 4, 5}));
    assert(search_sorted_matrix({{1, 4, 7}, {2, 5, 8}, {3, 6, 9}}, 6));
    assert(max_product_subarray({2, 3, -2, 4}) == 6);
    assert(longest_increasing_subsequence({10, 9, 2, 5, 3, 7, 101, 18}) == 4);
    assert(next_greater_element({2, 1, 2, 4, 3}) == vi({4, 2, 4, -1, -1}));
    assert(daily_temperatures({73, 74, 75, 71, 69, 72, 76, 73}) == vi({1, 1, 4, 2, 1, 1, 0, 0}));
    assert(largest_rectangle_histogram({2, 1, 5, 6, 2, 3}) == 10);
    assert(kth_largest_heap({3, 2, 1, 5, 6, 4}, 2) == 5);
    NumMatrix nm({{3, 0, 1, 4, 2}, {5, 6, 3, 2, 1}, {1, 2, 0, 1, 5},
                  {4, 1, 0, 1, 7}, {1, 0, 3, 0, 5}});
    assert(nm.sum_region(2, 1, 4, 3) == 8);
    cout << "Array revision tests passed!\\n";
}
#endif

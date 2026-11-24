// DSA REMAINING INTERVIEW TOPICS — C++17
// A compact reference for topics/patterns that complement the existing revision files.
// Compile snippets as a library; there is intentionally no main().
// Most snippets assume standard headers and using namespace std.

#include <bits/stdc++.h>
using namespace std;

namespace monotonic_structures {

// Next greater element to the right. O(n) time, O(n) space.
vector<int> nextGreaterRight(const vector<int>& a) {
    int n = (int)a.size();
    vector<int> ans(n, -1), st;
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && a[st.back()] < a[i]) {
            ans[st.back()] = a[i]; st.pop_back();
        }
        st.push_back(i);
    }
    return ans;
}

// Previous smaller element index (strictly smaller), -1 if absent.
vector<int> previousSmallerIndex(const vector<int>& a) {
    vector<int> ans(a.size(), -1), st;
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back();
        st.push_back(i);
    }
    return ans;
}

// Largest rectangle in histogram. O(n).
long long largestRectangle(const vector<int>& h) {
    int n = (int)h.size();
    vector<int> st;
    long long best = 0;
    for (int i = 0; i <= n; ++i) {
        int cur = (i == n ? 0 : h[i]);
        while (!st.empty() && h[st.back()] > cur) {
            int height = h[st.back()]; st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, 1LL * height * (i - left - 1));
        }
        st.push_back(i);
    }
    return best;
}

// Sliding window maximum using a decreasing deque. O(n).
vector<int> slidingWindowMaximum(const vector<int>& a, int k) {
    if (k <= 0 || k > (int)a.size()) return {};
    deque<int> dq;
    vector<int> ans;
    for (int i = 0; i < (int)a.size(); ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) ans.push_back(a[dq.front()]);
    }
    return ans;
}

} // namespace monotonic_structures

namespace trie {

// Lowercase a-z trie. Adapt alphabet mapping for other character sets.
struct Node {
    array<int, 26> next;
    bool terminal = false;
    Node() { next.fill(-1); }
};

class Trie {
    vector<Node> nodes{1};
public:
    void insert(const string& s) {
        int v = 0;
        for (char c : s) {
            int x = c - 'a';
            if (nodes[v].next[x] == -1) {
                nodes[v].next[x] = (int)nodes.size();
                nodes.emplace_back();
            }
            v = nodes[v].next[x];
        }
        nodes[v].terminal = true;
    }
    bool search(const string& s) const {
        int v = 0;
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26 || nodes[v].next[x] == -1) return false;
            v = nodes[v].next[x];
        }
        return nodes[v].terminal;
    }
    bool startsWith(const string& prefix) const {
        int v = 0;
        for (char c : prefix) {
            int x = c - 'a';
            if (x < 0 || x >= 26 || nodes[v].next[x] == -1) return false;
            v = nodes[v].next[x];
        }
        return true;
    }
};

// Maximum XOR with a stored 32-bit value; unsigned bit handling.
class BinaryTrie {
    struct Node { int child[2] = {-1, -1}; };
    vector<Node> t{1};
public:
    void insert(uint32_t x) {
        int v = 0;
        for (int b = 31; b >= 0; --b) {
            int bit = (x >> b) & 1U;
            if (t[v].child[bit] == -1) {
                t[v].child[bit] = (int)t.size(); t.emplace_back();
            }
            v = t[v].child[bit];
        }
    }
    uint32_t maxXor(uint32_t x) const {
        if (t.size() == 1) return 0;
        int v = 0; uint32_t result = 0;
        for (int b = 31; b >= 0; --b) {
            int bit = (x >> b) & 1U, want = bit ^ 1;
            if (t[v].child[want] != -1) {
                result |= (1U << b); v = t[v].child[want];
            } else v = t[v].child[bit];
        }
        return result;
    }
};

} // namespace trie

namespace string_algorithms {

// Prefix function / KMP. pi[i] = longest proper prefix that is suffix of s[0..i].
vector<int> prefixFunction(const string& s) {
    int n = (int)s.size(); vector<int> pi(n);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    return pi;
}

// All starting positions where pattern occurs in text. O(n + m).
vector<int> kmpSearch(const string& text, const string& pattern) {
    if (pattern.empty()) return {};
    vector<int> pi = prefixFunction(pattern), ans;
    for (int i = 0, j = 0; i < (int)text.size(); ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == (int)pattern.size()) {
            ans.push_back(i - j + 1); j = pi[j - 1];
        }
    }
    return ans;
}

// Z-function: z[i] = longest substring starting at i matching string prefix.
vector<int> zFunction(const string& s) {
    int n = (int)s.size(); vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        if (i + z[i] - 1 > r) l = i, r = i + z[i] - 1;
    }
    if (n) z[0] = n;
    return z;
}

// Rolling hash (double modulus reduces collision risk; never mathematically eliminates it).
class DoubleHash {
    static constexpr long long M1 = 1'000'000'007LL, M2 = 1'000'000'009LL;
    static constexpr long long B = 911382323LL;
    vector<long long> h1, h2, p1, p2;
public:
    explicit DoubleHash(const string& s) {
        int n = (int)s.size(); h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        for (int i = 0; i < n; ++i) {
            int x = (unsigned char)s[i] + 1;
            h1[i + 1] = (h1[i] * B + x) % M1;
            h2[i + 1] = (h2[i] * B + x) % M2;
            p1[i + 1] = p1[i] * B % M1; p2[i + 1] = p2[i] * B % M2;
        }
    }
    pair<long long,long long> get(int l, int r) const { // half-open [l,r)
        long long x = (h1[r] - h1[l] * p1[r-l] % M1 + M1) % M1;
        long long y = (h2[r] - h2[l] * p2[r-l] % M2 + M2) % M2;
        return {x, y};
    }
};

} // namespace string_algorithms

namespace graph_advanced {

// Kosaraju SCC: O(V + E). Returns component id for each vertex.
vector<int> kosarajuSCC(int n, const vector<vector<int>>& g) {
    vector<vector<int>> rg(n);
    for (int u = 0; u < n; ++u) for (int v : g[u]) rg[v].push_back(u);
    vector<char> seen(n, false); vector<int> order;
    function<void(int)> dfs1 = [&](int u) {
        seen[u] = true;
        for (int v : g[u]) if (!seen[v]) dfs1(v);
        order.push_back(u);
    };
    for (int i = 0; i < n; ++i) if (!seen[i]) dfs1(i);
    vector<int> comp(n, -1); int cid = 0;
    function<void(int)> dfs2 = [&](int u) {
        comp[u] = cid;
        for (int v : rg[u]) if (comp[v] == -1) dfs2(v);
    };
    reverse(order.begin(), order.end());
    for (int u : order) if (comp[u] == -1) dfs2(u), ++cid;
    return comp;
}

// Bridges in an undirected graph; edge IDs handle parallel edges correctly.
vector<pair<int,int>> bridges(int n, const vector<pair<int,int>>& edges) {
    vector<vector<pair<int,int>>> g(n);
    for (int id = 0; id < (int)edges.size(); ++id) {
        auto [u,v] = edges[id]; g[u].push_back({v,id}); g[v].push_back({u,id});
    }
    vector<int> tin(n, -1), low(n); int timer = 0;
    vector<pair<int,int>> ans;
    function<void(int,int)> dfs = [&](int u, int parentEdge) {
        tin[u] = low[u] = timer++;
        for (auto [v,id] : g[u]) {
            if (id == parentEdge) continue;
            if (tin[v] != -1) low[u] = min(low[u], tin[v]);
            else {
                dfs(v, id); low[u] = min(low[u], low[v]);
                if (low[v] > tin[u]) ans.push_back({u,v});
            }
        }
    };
    for (int i = 0; i < n; ++i) if (tin[i] == -1) dfs(i, -1);
    return ans;
}

// Articulation points in an undirected graph.
vector<int> articulationPoints(int n, const vector<vector<int>>& g) {
    vector<int> tin(n, -1), low(n); vector<char> cut(n, false); int timer = 0;
    function<void(int,int)> dfs = [&](int u, int p) {
        tin[u] = low[u] = timer++; int children = 0;
        for (int v : g[u]) {
            if (v == p) continue;
            if (tin[v] != -1) low[u] = min(low[u], tin[v]);
            else {
                dfs(v, u); low[u] = min(low[u], low[v]); ++children;
                if (p != -1 && low[v] >= tin[u]) cut[u] = true;
            }
        }
        if (p == -1 && children > 1) cut[u] = true;
    };
    for (int i = 0; i < n; ++i) if (tin[i] == -1) dfs(i, -1);
    vector<int> ans;
    for (int i = 0; i < n; ++i) if (cut[i]) ans.push_back(i);
    return ans;
}

// 0-1 BFS: edge weights must be exactly 0 or 1. O(V + E).
vector<int> zeroOneBFS(int n, const vector<vector<pair<int,int>>>& g, int source) {
    const int INF = INT_MAX / 2; vector<int> dist(n, INF);
    deque<int> dq; dist[source] = 0; dq.push_front(source);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto [v,w] : g[u]) if (dist[v] > dist[u] + w) {
            dist[v] = dist[u] + w;
            if (w == 0) dq.push_front(v); else dq.push_back(v);
        }
    }
    return dist;
}

} // namespace graph_advanced

namespace range_queries {

// Sparse table for idempotent operations such as min/max/gcd. O(n log n) build, O(1) query.
class SparseTableMin {
    vector<vector<int>> st; vector<int> lg;
public:
    explicit SparseTableMin(const vector<int>& a) {
        int n = (int)a.size(); lg.assign(n + 1, 0);
        for (int i = 2; i <= n; ++i) lg[i] = lg[i / 2] + 1;
        if (!n) return;
        st.assign(lg[n] + 1, vector<int>(n)); st[0] = a;
        for (int k = 1; k < (int)st.size(); ++k)
            for (int i = 0; i + (1 << k) <= n; ++i)
                st[k][i] = min(st[k-1][i], st[k-1][i + (1 << (k-1))]);
    }
    int query(int l, int r) const { // inclusive [l,r]
        int k = lg[r - l + 1];
        return min(st[k][l], st[k][r - (1 << k) + 1]);
    }
};

// Sqrt decomposition for range sum with point updates. O(sqrt(n)) each.
class SqrtSum {
    int n, block; vector<long long> a, sums;
public:
    explicit SqrtSum(const vector<int>& input) : n((int)input.size()), block(max(1, (int)sqrt(max(1, (int)input.size())))), a(n), sums((n + block - 1) / block) {
        for (int i = 0; i < n; ++i) a[i] = input[i], sums[i / block] += a[i];
    }
    void update(int i, long long value) {
        sums[i / block] += value - a[i]; a[i] = value;
    }
    long long query(int l, int r) const { // inclusive
        long long ans = 0;
        while (l <= r && l % block != 0) ans += a[l++];
        while (l + block - 1 <= r) ans += sums[l / block], l += block;
        while (l <= r) ans += a[l++];
        return ans;
    }
};

} // namespace range_queries

namespace randomized_algorithms {

// Randomized Quickselect: kth smallest, 0-indexed. Expected O(n), worst O(n^2).
int kthSmallest(vector<int> a, int k) {
    if (k < 0 || k >= (int)a.size()) throw out_of_range("k out of range");
    mt19937 rng((uint32_t)chrono::steady_clock::now().time_since_epoch().count());
    int left = 0, right = (int)a.size() - 1;
    while (left <= right) {
        int pivotIndex = uniform_int_distribution<int>(left, right)(rng);
        int pivot = a[pivotIndex]; swap(a[pivotIndex], a[right]);
        int store = left;
        for (int i = left; i < right; ++i) if (a[i] < pivot) swap(a[i], a[store++]);
        swap(a[store], a[right]);
        if (store == k) return a[store];
        if (store < k) left = store + 1; else right = store - 1;
    }
    throw logic_error("unreachable");
}

} // namespace randomized_algorithms

/*
ADDITIONAL TOPICS TO KNOW CONCEPTUALLY (implement when relevant):

1. Graphs:
   - Bellman-Ford and negative-cycle detection; Floyd-Warshall all-pairs shortest paths
   - Dijkstra correctness conditions; DAG shortest/longest paths
   - Maximum flow (Edmonds-Karp / Dinic), min-cut theorem
   - Eulerian paths/circuits (Hierholzer), Hamiltonian path is generally hard
   - Bipartite matching (Kuhn / Hopcroft-Karp), tree rerooting DP
   - 2-SAT (implication graph + SCC)

2. Strings:
   - Aho-Corasick for many-pattern matching
   - Suffix array + LCP, suffix automaton, Manacher's palindrome radii
   - Palindrome partitioning / eertree for advanced string problems

3. Data structures:
   - Order-statistics tree (GNU PBDS is GCC-specific, not standard C++)
   - Persistent segment tree, implicit/dynamic segment tree
   - Link-cut tree / HLD for tree path queries (advanced)
   - DSU rollback for offline dynamic connectivity

4. Problem-solving techniques:
   - Coordinate compression, offline queries, sweep line
   - Meet-in-the-middle, bitset optimization, SOS DP
   - Invariant/proof, amortized analysis, adversarial cases
   - Numeric safety: overflow, signed/unsigned, modulo arithmetic

INTERVIEW PRIORITY:
High: monotonic stack/deque, trie, KMP/Z, SCC, bridges/articulation, 0-1 BFS,
      sparse table, coordinate compression, sweep line, randomized quickselect.
Medium/advanced: Aho-Corasick, suffix array, max-flow, matching, 2-SAT, persistent DS.
*/

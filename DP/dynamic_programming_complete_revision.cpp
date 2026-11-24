// DYNAMIC PROGRAMMING — COMPLETE INTERVIEW REVISION (C++17)
// Source reference: dynamic_programming_complete_revision.py
// Compile: g++ -std=c++17 -O2 -Wall -Wextra -c dynamic_programming_complete_revision.cpp
//
// DP checklist: state meaning -> transition -> base cases -> iteration order -> answer -> optimize.
// This is a reusable library; remove/rename duplicate signatures when merging into a solution.

#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF64 = (1LL << 60);

// 1. Fibonacci, stairs, cost stairs
ll fibonacci(int n) {
    if (n <= 1) return n;
    ll a = 0, b = 1;
    for (int i = 2; i <= n; ++i) { ll c = a + b; a = b; b = c; }
    return b;
}
ll climbingStairs(int n) {
    if (n <= 2) return n;
    ll a = 1, b = 2;
    for (int i = 3; i <= n; ++i) { ll c = a + b; a = b; b = c; }
    return b;
}
ll climbingKSteps(int n, int k) {
    vector<ll> dp(n + 1); dp[0] = 1;
    for (int i = 1; i <= n; ++i)
        for (int step = 1; step <= k && step <= i; ++step) dp[i] += dp[i-step];
    return dp[n];
}
ll minCostClimbingStairs(const vector<int>& cost) {
    int n = (int)cost.size(); if (!n) return 0;
    ll prev2 = 0, prev1 = 0;
    for (int i = 0; i < n; ++i) { ll cur = cost[i] + min(prev1, prev2); prev2 = prev1; prev1 = cur; }
    return min(prev1, prev2);
}

// 2. House robber, circular robber, Kadane
ll houseRobber(const vector<int>& a) {
    ll prev2 = 0, prev1 = 0;
    for (int x : a) { ll cur = max(prev1, prev2 + x); prev2 = prev1; prev1 = cur; }
    return prev1;
}
ll houseRobberII(const vector<int>& a) {
    int n = (int)a.size(); if (!n) return 0; if (n == 1) return a[0];
    auto rangeRob = [&](int l, int r) { ll x=0,y=0; for(int i=l;i<=r;++i){ll z=max(y,x+a[i]);x=y;y=z;} return y; };
    return max(rangeRob(0,n-2), rangeRob(1,n-1));
}
ll maxSubarray(const vector<int>& a) {
    if (a.empty()) return 0;
    ll cur=a[0], best=a[0];
    for (int i=1;i<(int)a.size();++i) { cur=max<ll>(a[i],cur+a[i]); best=max(best,cur); }
    return best;
}
tuple<ll,int,int> maxSubarrayWithIndices(const vector<int>& a) {
    if (a.empty()) return {0,-1,-1};
    ll cur=a[0], best=a[0]; int start=0, bl=0, br=0;
    for(int i=1;i<(int)a.size();++i) {
        if ((ll)a[i] > cur+a[i]) { cur=a[i]; start=i; } else cur+=a[i];
        if(cur>best){best=cur;bl=start;br=i;}
    }
    return {best,bl,br};
}

// 3. Jump game (greedy optimal), Decode Ways
bool canJump(const vector<int>& a) {
    int reach=0; for(int i=0;i<(int)a.size();++i){if(i>reach)return false;reach=max(reach,i+a[i]);} return true;
}
int jumpGameII(const vector<int>& a) {
    if(a.size()<=1)return 0; int jumps=0,end=0,far=0;
    for(int i=0;i<(int)a.size()-1;++i){far=max(far,i+a[i]);if(i==end){++jumps;end=far;}}
    return jumps;
}
ll decodeWays(const string& s) {
    if(s.empty()||s[0]=='0')return 0; ll p2=1,p1=1;
    for(int i=1;i<(int)s.size();++i){ll cur=0;if(s[i]!='0')cur+=p1;
        int two=(s[i-1]-'0')*10+(s[i]-'0');if(two>=10&&two<=26)cur+=p2;p2=p1;p1=cur;}
    return p1;
}

// 4. Knapsack family
ll knapsack01(const vector<int>& w,const vector<int>& v,int cap) {
    vector<ll> dp(cap+1); for(int i=0;i<(int)w.size();++i)
        for(int c=cap;c>=w[i];--c) dp[c]=max(dp[c],dp[c-w[i]]+v[i]); return dp[cap];
}
ll unboundedKnapsack(const vector<int>& w,const vector<int>& v,int cap) {
    vector<ll> dp(cap+1); for(int i=0;i<(int)w.size();++i)
        for(int c=w[i];c<=cap;++c) dp[c]=max(dp[c],dp[c-w[i]]+v[i]); return dp[cap];
}
bool subsetSum(const vector<int>& a,int target) {
    vector<char> dp(target+1);dp[0]=1;for(int x:a)for(int s=target;s>=x;--s)dp[s]=dp[s]||dp[s-x];return dp[target];
}
bool canPartitionEqual(const vector<int>& a) {
    int sum=accumulate(a.begin(),a.end(),0);return sum%2==0&&subsetSum(a,sum/2);
}
ll targetSumWays(const vector<int>& a,int target) {
    unordered_map<int,ll> dp{{0,1}};
    for(int x:a){unordered_map<int,ll> nd;for(auto [s,c]:dp){nd[s+x]+=c;nd[s-x]+=c;}dp.swap(nd);}
    return dp.count(target)?dp[target]:0;
}
int coinChangeMin(const vector<int>& coins,int amount) {
    vector<int> dp(amount+1,amount+1);dp[0]=0;
    for(int x=1;x<=amount;++x)for(int c:coins)if(c<=x)dp[x]=min(dp[x],dp[x-c]+1);
    return dp[amount]==amount+1?-1:dp[amount];
}
ll coinChangeCombinations(int amount,const vector<int>& coins) {
    vector<ll> dp(amount+1);dp[0]=1;for(int c:coins)for(int x=c;x<=amount;++x)dp[x]+=dp[x-c];return dp[amount];
}
ll rodCutting(const vector<int>& price,int n) {
    vector<ll> dp(n+1);for(int len=1;len<=n;++len)for(int cut=1;cut<=len&&cut<=(int)price.size();++cut)
        dp[len]=max(dp[len],(ll)price[cut-1]+dp[len-cut]);return dp[n];
}

// 5. LIS and common-subsequence family
int lisN2(const vector<int>& a) {
    int n=a.size();if(!n)return 0;vector<int> dp(n,1);int ans=1;
    for(int i=0;i<n;++i)for(int j=0;j<i;++j)if(a[j]<a[i])dp[i]=max(dp[i],dp[j]+1);
    return *max_element(dp.begin(),dp.end());
}
int lisNlogN(const vector<int>& a) {
    vector<int> tails;for(int x:a){auto it=lower_bound(tails.begin(),tails.end(),x);if(it==tails.end())tails.push_back(x);else *it=x;}return tails.size();
}
vector<int> reconstructLIS(const vector<int>& a) {
    int n=a.size();if(!n)return {};vector<int> tails,tailIdx,parent(n,-1);
    for(int i=0;i<n;++i){int p=lower_bound(tails.begin(),tails.end(),a[i])-tails.begin();
        if(p==(int)tails.size()){tails.push_back(a[i]);tailIdx.push_back(i);}else{tails[p]=a[i];tailIdx[p]=i;}
        if(p)parent[i]=tailIdx[p-1];}
    vector<int> out;for(int i=tailIdx.back();i!=-1;i=parent[i])out.push_back(a[i]);reverse(out.begin(),out.end());return out;
}
int numberOfLIS(const vector<int>& a) {
    int n=a.size();if(!n)return 0;vector<int> len(n,1),cnt(n,1);
    for(int i=0;i<n;++i)for(int j=0;j<i;++j)if(a[j]<a[i]){
        if(len[j]+1>len[i])len[i]=len[j]+1,cnt[i]=cnt[j];else if(len[j]+1==len[i])cnt[i]+=cnt[j];}
    int L=*max_element(len.begin(),len.end()),ans=0;for(int i=0;i<n;++i)if(len[i]==L)ans+=cnt[i];return ans;
}
int lcs(const string& a,const string& b) {
    int n=a.size(),m=b.size();vector<vector<int>> dp(n+1,vector<int>(m+1));
    for(int i=n-1;i>=0;--i)for(int j=m-1;j>=0;--j)dp[i][j]=a[i]==b[j]?1+dp[i+1][j+1]:max(dp[i+1][j],dp[i][j+1]);return dp[0][0];
}
string reconstructLCS(const string& a,const string& b) {
    int n=a.size(),m=b.size();vector<vector<int>> dp(n+1,vector<int>(m+1));
    for(int i=n-1;i>=0;--i)for(int j=m-1;j>=0;--j)dp[i][j]=a[i]==b[j]?1+dp[i+1][j+1]:max(dp[i+1][j],dp[i][j+1]);
    string s;int i=0,j=0;while(i<n&&j<m){if(a[i]==b[j])s+=a[i++],++j;else if(dp[i+1][j]>=dp[i][j+1])++i;else ++j;}return s;
}
int longestCommonSubstring(const string& a,const string& b) {
    int n=a.size(),m=b.size(),ans=0;vector<int> prev(m+1),cur(m+1);
    for(int i=1;i<=n;++i){fill(cur.begin(),cur.end(),0);for(int j=1;j<=m;++j)if(a[i-1]==b[j-1])ans=max(ans,cur[j]=prev[j-1]+1);prev.swap(cur);}return ans;
}
int editDistance(const string& a,const string& b) {
    int m=b.size();vector<int> prev(m+1),cur(m+1);iota(prev.begin(),prev.end(),0);
    for(int i=1;i<=(int)a.size();++i){cur[0]=i;for(int j=1;j<=m;++j)cur[j]=a[i-1]==b[j-1]?prev[j-1]:1+min({prev[j],cur[j-1],prev[j-1]});prev.swap(cur);}return prev[m];
}
ll distinctSubsequences(const string& s,const string& t) {
    vector<ll> dp(t.size()+1);dp[0]=1;for(char c:s)for(int j=(int)t.size()-1;j>=0;--j)if(c==t[j])dp[j+1]+=dp[j];return dp.back();
}
bool wordBreak(const string& s,const vector<string>& dict) {
    unordered_set<string> words(dict.begin(),dict.end());vector<char> dp(s.size()+1);dp[0]=1;
    for(int i=1;i<=(int)s.size();++i)for(int j=0;j<i;++j)if(dp[j]&&words.count(s.substr(j,i-j))){dp[i]=1;break;}return dp.back();
}

// 6. Grid DP
ll uniquePaths(int m,int n) {
    if(m<=0||n<=0)return 0;vector<ll> dp(n,1);for(int r=1;r<m;++r)for(int c=1;c<n;++c)dp[c]+=dp[c-1];return dp.back();
}
ll uniquePathsObstacles(const vector<vector<int>>& g) {
    if(g.empty()||g[0].empty())return 0;int m=g.size(),n=g[0].size();vector<ll> dp(n);dp[0]=1;
    for(int r=0;r<m;++r)for(int c=0;c<n;++c)if(g[r][c])dp[c]=0;else if(c)dp[c]+=dp[c-1];return dp.back();
}
ll minPathSum(const vector<vector<int>>& g) {
    if(g.empty()||g[0].empty())return 0;int n=g[0].size();vector<ll> dp(n+1,INF64);dp[1]=0;
    for(auto& row:g)for(int c=1;c<=n;++c)dp[c]=row[c-1]+min(dp[c],dp[c-1]);return dp[n];
}
ll minFallingPathSum(const vector<vector<int>>& a) {
    if(a.empty())return 0;int n=a[0].size();vector<ll> p(a[0].begin(),a[0].end());
    for(int r=1;r<(int)a.size();++r){vector<ll> c(n,INF64);for(int j=0;j<n;++j){c[j]=p[j];if(j)c[j]=min(c[j],p[j-1]);if(j+1<n)c[j]=min(c[j],p[j+1]);c[j]+=a[r][j];}p.swap(c);}return *min_element(p.begin(),p.end());
}
int maximalSquare(const vector<string>& a) {
    if(a.empty())return 0;int n=a[0].size(),best=0;vector<int> p(n+1),c(n+1);
    for(auto& row:a){fill(c.begin(),c.end(),0);for(int j=1;j<=n;++j)if(row[j-1]=='1')best=max(best,c[j]=1+min({p[j],c[j-1],p[j-1]}));p.swap(c);}return best*best;
}

// 7. Interval DP
ll matrixChainMultiplication(const vector<int>& d) {
    int n=(int)d.size()-1;if(n<=1)return 0;vector<vector<ll>> dp(n,vector<ll>(n));
    for(int len=2;len<=n;++len)for(int i=0;i+len<=n;++i){int j=i+len-1;dp[i][j]=INF64;
        for(int k=i;k<j;++k)dp[i][j]=min(dp[i][j],dp[i][k]+dp[k+1][j]+1LL*d[i]*d[k+1]*d[j+1]);}return dp[0][n-1];
}
ll burstBalloons(const vector<int>& nums) {
    vector<ll> a{1};for(int x:nums)a.push_back(x);a.push_back(1);int n=a.size();vector<vector<ll>> dp(n,vector<ll>(n));
    for(int len=2;len<n;++len)for(int l=0;l+len<n;++l){int r=l+len;for(int k=l+1;k<r;++k)dp[l][r]=max(dp[l][r],dp[l][k]+dp[k][r]+a[l]*a[k]*a[r]);}return dp[0][n-1];
}

// 8. Stock state DP
ll stockOne(const vector<int>& p) {ll mn=INF64,ans=0;for(ll x:p){mn=min(mn,x);ans=max(ans,x-mn);}return ans;}
ll stockUnlimited(const vector<int>& p) {ll ans=0;for(int i=1;i<(int)p.size();++i)ans+=max(0,p[i]-p[i-1]);return ans;}
ll stockWithFee(const vector<int>& p,int fee) {
    if(p.empty())return 0;ll cash=0,hold=-p[0];for(int i=1;i<(int)p.size();++i){ll old=cash;cash=max(cash,hold+p[i]-fee);hold=max(hold,old-p[i]);}return cash;
}
ll stockCooldown(const vector<int>& p) {
    if(p.empty())return 0;ll hold=-p[0],sold=0,rest=0;
    for(int i=1;i<(int)p.size();++i){ll h=hold,s=sold,r=rest;hold=max(h,r-p[i]);sold=h+p[i];rest=max(r,s);}return max(sold,rest);
}
ll stockAtMostTwo(const vector<int>& p) {
    ll b1=-INF64,s1=0,b2=-INF64,s2=0;for(ll x:p){b1=max(b1,-x);s1=max(s1,b1+x);b2=max(b2,s1-x);s2=max(s2,b2+x);}return s2;
}

// 9. Tree DP helpers
struct TreeNode { int val; TreeNode *left,*right; explicit TreeNode(int x):val(x),left(nullptr),right(nullptr){} };
ll houseRobberTree(TreeNode* root) {
    function<pair<ll,ll>(TreeNode*)> dfs=[&](TreeNode* n)->pair<ll,ll>{if(!n)return {0,0};auto [lr,ls]=dfs(n->left);auto [rr,rs]=dfs(n->right);return {n->val+ls+rs,max(lr,ls)+max(rr,rs)};};
    auto [rob,skip]=dfs(root);return max(rob,skip);
}
ll maximumPathSumTree(TreeNode* root) {
    ll best=-INF64;function<ll(TreeNode*)> dfs=[&](TreeNode* n)->ll{if(!n)return 0;ll l=max(0LL,dfs(n->left)),r=max(0LL,dfs(n->right));best=max(best,l+r+n->val);return n->val+max(l,r);};dfs(root);return root?best:0;
}

// 10. DAG DP: longest path from source in directed acyclic graph
vector<ll> dagLongestPath(int n,const vector<vector<pair<int,int>>>& g,int source) {
    vector<int> indeg(n);for(int u=0;u<n;++u)for(auto [v,w]:g[u])++indeg[v];
    queue<int> q;for(int i=0;i<n;++i)if(!indeg[i])q.push(i);vector<int> order;
    while(!q.empty()){int u=q.front();q.pop();order.push_back(u);for(auto [v,w]:g[u])if(--indeg[v]==0)q.push(v);}
    vector<ll> d(n,-INF64);d[source]=0;for(int u:order)if(d[u]!=-INF64)for(auto [v,w]:g[u])d[v]=max(d[v],d[u]+w);return d;
}

// 11. Bitmask DP: assignment minimum cost, O(n*2^n)
ll assignmentMinCost(const vector<vector<int>>& cost) {
    int n=cost.size();vector<ll> dp(1<<n,INF64);dp[0]=0;
    for(int mask=0;mask<(1<<n);++mask){int person=__builtin_popcount((unsigned)mask);if(person>=n||dp[mask]==INF64)continue;
        for(int job=0;job<n;++job)if(!(mask>>job&1)){int nm=mask|1<<job;dp[nm]=min(dp[nm],dp[mask]+cost[person][job]);}}
    return dp.back();
}

// 12. Digit DP: count numbers in [0, bound] whose digit sum <= limit
ll countDigitSumAtMost(const string& bound,int limit) {
    int n=bound.size();vector<vector<ll>> memo(n+1,vector<ll>(limit+1,-1));
    function<ll(int,int,bool,bool)> dfs=[&](int pos,int sum,bool tight,bool started)->ll{
        if(sum>limit)return 0;if(pos==n)return 1;
        if(!tight&&started&&memo[pos][sum]!=-1)return memo[pos][sum];
        int hi=tight?bound[pos]-'0':9;ll ans=0;
        for(int d=0;d<=hi;++d)ans+=dfs(pos+1,sum+d,tight&&d==hi,started||d!=0);
        if(!tight&&started)memo[pos][sum]=ans;return ans;};
    return dfs(0,0,true,false);
}

// 13. Game DP: optimal play, score difference (pick ends)
ll optimalEndGameDifference(const vector<int>& a) {
    int n=a.size();vector<ll> dp(a.begin(),a.end());
    for(int len=2;len<=n;++len)for(int l=0;l+len<=n;++l){int r=l+len-1;dp[l]=max((ll)a[l]-dp[l+1],(ll)a[r]-dp[l]);}return n?dp[0]:0;
}

// 14. Reconstruction example: minimum coins path is represented by parent[]
// Pattern reminders:
// - 1D: dp[i] often depends on a small prefix.
// - Knapsack: descending capacity = 0/1; ascending = unbounded.
// - Interval: solve shorter intervals before longer ones.
// - Tree: return multiple states from DFS.
// - Bitmask: state encodes chosen subset.
// - Digit: position + tight + additional constraints.
// - Optimize only after state/transition are correct.

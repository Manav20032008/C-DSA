// GREEDY + ADVANCED DSA — INTERVIEW REVISION (C++17)
// Source reference: phase_2_greedy_advanced_revision.py
// Compile: g++ -std=c++17 -O2 -Wall -Wextra -c phase_2_greedy_advanced_revision.cpp

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 1. Greedy intervals and scheduling
vector<pair<int,int>> activitySelection(vector<pair<int,int>> a) {
    sort(a.begin(),a.end(),[](auto x,auto y){return x.second<y.second;});
    vector<pair<int,int>> chosen;int end=INT_MIN;
    for(auto [s,e]:a)if(s>=end)chosen.push_back({s,e}),end=e;return chosen;
}
int eraseOverlapIntervals(vector<pair<int,int>> a) {
    if(a.empty())return 0;sort(a.begin(),a.end(),[](auto x,auto y){return x.second<y.second;});
    int end=a[0].second,removed=0;for(int i=1;i<(int)a.size();++i)if(a[i].first<end)++removed;else end=a[i].second;return removed;
}
int minArrowShots(vector<pair<int,int>> p) {
    if(p.empty())return 0;sort(p.begin(),p.end(),[](auto x,auto y){return x.second<y.second;});
    int arrows=1,end=p[0].second;for(auto [s,e]:p)if(s>end)++arrows,end=e;return arrows;
}
int assignCookies(vector<int> greed,vector<int> cookies) {
    sort(greed.begin(),greed.end());sort(cookies.begin(),cookies.end());int i=0;
    for(int c:cookies)if(i<(int)greed.size()&&c>=greed[i])++i;return i;
}
bool canJump(const vector<int>& a){int reach=0;for(int i=0;i<(int)a.size();++i){if(i>reach)return false;reach=max(reach,i+a[i]);}return true;}
int minJumps(const vector<int>& a){if(a.size()<=1)return 0;int jumps=0,end=0,far=0;for(int i=0;i<(int)a.size()-1;++i){far=max(far,i+a[i]);if(i==end)++jumps,end=far;}return jumps;}
int gasStation(const vector<int>& gas,const vector<int>& cost){
    if(accumulate(gas.begin(),gas.end(),0)<accumulate(cost.begin(),cost.end(),0))return -1;
    int start=0,tank=0;for(int i=0;i<(int)gas.size();++i){tank+=gas[i]-cost[i];if(tank<0)start=i+1,tank=0;}return start;
}
ll candyDistribution(const vector<int>& rating){
    int n=rating.size();if(!n)return 0;vector<int> c(n,1);
    for(int i=1;i<n;++i)if(rating[i]>rating[i-1])c[i]=c[i-1]+1;
    for(int i=n-2;i>=0;--i)if(rating[i]>rating[i+1])c[i]=max(c[i],c[i+1]+1);
    return accumulate(c.begin(),c.end(),0LL);
}
string removeKDigits(string s,int k){
    string st;for(char c:s){while(k&&!st.empty()&&st.back()>c)st.pop_back(),--k;st.push_back(c);}
    if(k<(int)st.size())st.resize(st.size()-k);else st.clear();int i=0;while(i<(int)st.size()&&st[i]=='0')++i;st=st.substr(i);return st.empty()?"0":st;
}
string reorganizeString(const string& s){
    vector<int> f(256);for(unsigned char c:s)++f[c];priority_queue<pair<int,char>> pq;for(int c=0;c<256;++c)if(f[c])pq.push({f[c],(char)c});
    string out;pair<int,char> prev={0,'#'};
    while(!pq.empty()){auto [cnt,ch]=pq.top();pq.pop();out+=ch;--cnt;if(prev.first>0)pq.push(prev);prev={cnt,ch};}
    return out.size()==s.size()?out:"";
}
int taskScheduler(vector<char> tasks,int cooldown){
    vector<int> f(256);for(unsigned char c:tasks)++f[c];int mx=*max_element(f.begin(),f.end()),num=count(f.begin(),f.end(),mx);
    return max((int)tasks.size(),(mx-1)*(cooldown+1)+num);
}
pair<ll,vector<string>> jobSequencing(vector<tuple<string,int,int>> jobs){
    sort(jobs.begin(),jobs.end(),[](auto&a,auto&b){return get<2>(a)>get<2>(b);});int md=0;for(auto&j:jobs)md=max(md,get<1>(j));
    vector<string> slot(md+1);ll profit=0;vector<string> selected;
    for(auto&[id,d,p]:jobs)for(int t=min(d,md);t>=1;--t)if(slot[t].empty()){slot[t]=id;profit+=p;selected.push_back(id);break;}
    return {profit,selected};
}

// Huffman tree and code generation
struct HuffmanNode { char ch; ll freq; HuffmanNode *left,*right; HuffmanNode(char c,ll f):ch(c),freq(f),left(nullptr),right(nullptr){} };
struct HuffmanCmp { bool operator()(HuffmanNode* a,HuffmanNode* b)const{return a->freq>b->freq;} };
HuffmanNode* buildHuffmanTree(const string& s){
    int f[256]={};for(unsigned char c:s)++f[c];priority_queue<HuffmanNode*,vector<HuffmanNode*>,HuffmanCmp> pq;
    for(int i=0;i<256;++i)if(f[i])pq.push(new HuffmanNode((char)i,f[i]));if(pq.empty())return nullptr;
    while(pq.size()>1){auto a=pq.top();pq.pop();auto b=pq.top();pq.pop();auto p=new HuffmanNode('\0',a->freq+b->freq);p->left=a;p->right=b;pq.push(p);}return pq.top();
}
void huffmanCodes(HuffmanNode* root,string path,map<char,string>& codes){
    if(!root)return;if(!root->left&&!root->right){codes[root->ch]=path.empty()?"0":path;return;}
    huffmanCodes(root->left,path+"0",codes);huffmanCodes(root->right,path+"1",codes);
}

// 2. Bit manipulation
int getBit(int n,int i){return (n>>i)&1;}
int setBit(int n,int i){return n|(1<<i);}
int clearBit(int n,int i){return n&~(1<<i);}
int toggleBit(int n,int i){return n^(1<<i);}
int clearLowestSetBit(int n){return n&(n-1);}
int lowestSetBit(int n){return n&-n;}
bool isPowerOfTwo(int n){return n>0&&(n&(n-1))==0;}
int countSetBits(unsigned int n){int c=0;while(n)n&=n-1,++c;return c;}
int singleNumber(const vector<int>& a){int x=0;for(int v:a)x^=v;return x;}
int missingNumber(const vector<int>& a){int x=a.size();for(int i=0;i<(int)a.size();++i)x^=i^a[i];return x;}
vector<int> singleNumberIII(const vector<int>& a){int x=0;for(int v:a)x^=v;int bit=x&-x,u=0,v=0;for(int z:a)if(z&bit)u^=z;else v^=z;return {u,v};}
uint32_t reverseBits32(uint32_t n){uint32_t r=0;for(int i=0;i<32;++i)r=(r<<1)|(n&1),n>>=1;return r;}
int hammingDistance(int x,int y){return countSetBits((unsigned)(x^y));}
int xorPrefix(int n){if(n%4==0)return n;if(n%4==1)return 1;if(n%4==2)return n+1;return 0;}
int xorRange(int l,int r){return xorPrefix(r)^xorPrefix(l-1);}
vector<vector<int>> subsetsBitmask(const vector<int>& a){vector<vector<int>> out;for(int m=0;m<(1<<a.size());++m){vector<int>s;for(int i=0;i<(int)a.size();++i)if(m>>i&1)s.push_back(a[i]);out.push_back(s);}return out;}
vector<int> enumerateSubmasks(int mask){vector<int> v;for(int s=mask;;s=(s-1)&mask){v.push_back(s);if(!s)break;}return v;}

// 3. Fenwick tree / BIT (0-indexed API)
struct FenwickTree {
    int n;vector<ll> bit;explicit FenwickTree(int n):n(n),bit(n+1){}
    void add(int i,ll delta){for(++i;i<=n;i+=i&-i)bit[i]+=delta;}
    ll prefixSum(int i)const{ll s=0;for(++i;i>0;i-=i&-i)s+=bit[i];return s;}
    ll rangeSum(int l,int r)const{return l>r?0:prefixSum(r)-(l?prefixSum(l-1):0);}
};

// 4. Segment tree: range sum + point assignment; lazy range add + range sum
struct SegmentTree {
    int n;vector<ll> tree;explicit SegmentTree(const vector<int>& a):n(a.size()),tree(4*max(1,(int)a.size())){if(n)build(1,0,n-1,a);}
    void build(int v,int l,int r,const vector<int>&a){if(l==r){tree[v]=a[l];return;}int m=(l+r)/2;build(v*2,l,m,a);build(v*2+1,m+1,r,a);tree[v]=tree[v*2]+tree[v*2+1];}
    void update(int idx,ll val,int v,int l,int r){if(l==r){tree[v]=val;return;}int m=(l+r)/2;if(idx<=m)update(idx,val,v*2,l,m);else update(idx,val,v*2+1,m+1,r);tree[v]=tree[v*2]+tree[v*2+1];}
    ll query(int ql,int qr,int v,int l,int r)const{if(qr<l||r<ql)return 0;if(ql<=l&&r<=qr)return tree[v];int m=(l+r)/2;return query(ql,qr,v*2,l,m)+query(ql,qr,v*2+1,m+1,r);}
    void update(int idx,ll val){if(n)update(idx,val,1,0,n-1);}ll query(int l,int r)const{return n?query(l,r,1,0,n-1):0;}
};
struct LazySegmentTree {
    int n;vector<ll> tree,lazy;explicit LazySegmentTree(const vector<int>&a):n(a.size()),tree(4*max(1,(int)a.size())),lazy(tree.size()){if(n)build(1,0,n-1,a);}
    void build(int v,int l,int r,const vector<int>&a){if(l==r){tree[v]=a[l];return;}int m=(l+r)/2;build(v*2,l,m,a);build(v*2+1,m+1,r,a);tree[v]=tree[v*2]+tree[v*2+1];}
    void apply(int v,int l,int r,ll x){tree[v]+=(r-l+1)*x;lazy[v]+=x;}
    void push(int v,int l,int r){if(!lazy[v]||l==r)return;int m=(l+r)/2;apply(v*2,l,m,lazy[v]);apply(v*2+1,m+1,r,lazy[v]);lazy[v]=0;}
    void add(int ql,int qr,ll x,int v,int l,int r){if(qr<l||r<ql)return;if(ql<=l&&r<=qr){apply(v,l,r,x);return;}push(v,l,r);int m=(l+r)/2;add(ql,qr,x,v*2,l,m);add(ql,qr,x,v*2+1,m+1,r);tree[v]=tree[v*2]+tree[v*2+1];}
    ll sum(int ql,int qr,int v,int l,int r){if(qr<l||r<ql)return 0;if(ql<=l&&r<=qr)return tree[v];push(v,l,r);int m=(l+r)/2;return sum(ql,qr,v*2,l,m)+sum(ql,qr,v*2+1,m+1,r);}
    void rangeAdd(int l,int r,ll x){if(n)add(l,r,x,1,0,n-1);}ll rangeSum(int l,int r){return n?sum(l,r,1,0,n-1):0;}
};

// 5. DSU / Union-Find + Kruskal MST
struct DSU {
    vector<int> p,sz;int components;explicit DSU(int n):p(n),sz(n,1),components(n){iota(p.begin(),p.end(),0);}
    int find(int x){return p[x]==x?x:p[x]=find(p[x]);}
    bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);p[b]=a;sz[a]+=sz[b];--components;return true;}
    bool connected(int a,int b){return find(a)==find(b);}
};
pair<ll,vector<tuple<int,int,int>>> kruskalMST(int n,vector<tuple<int,int,int>> edges){
    sort(edges.begin(),edges.end(),[](auto&a,auto&b){return get<2>(a)<get<2>(b);});DSU d(n);ll cost=0;vector<tuple<int,int,int>> chosen;
    for(auto [u,v,w]:edges)if(d.unite(u,v))cost+=w,chosen.push_back({u,v,w});if((int)chosen.size()!=n-1)return {LLONG_MAX,chosen};return {cost,chosen};
}

// 6. Divide & conquer
vector<int> mergeSort(vector<int>a){if(a.size()<=1)return a;int m=a.size()/2;vector<int>l(a.begin(),a.begin()+m),r(a.begin()+m,a.end());l=mergeSort(l);r=mergeSort(r);vector<int>o;merge(l.begin(),l.end(),r.begin(),r.end(),back_inserter(o));return o;}
int quickselectKthLargest(vector<int>a,int k){int target=(int)a.size()-k,l=0,r=(int)a.size()-1;while(true){int pivot=a[r],p=l;for(int i=l;i<r;++i)if(a[i]<=pivot)swap(a[p++],a[i]);swap(a[p],a[r]);if(p==target)return a[p];if(p<target)l=p+1;else r=p-1;}}
ll maxSubarrayDivideConquer(const vector<int>&a){if(a.empty())return 0;function<ll(int,int)> f=[&](int l,int r)->ll{if(l==r)return a[l];int m=(l+r)/2;ll x=f(l,m),y=f(m+1,r),s=0,bl=LLONG_MIN,br=LLONG_MIN;for(int i=m;i>=l;--i)s+=a[i],bl=max(bl,s);s=0;for(int i=m+1;i<=r;++i)s+=a[i],br=max(br,s);return max({x,y,bl+br});};return f(0,(int)a.size()-1);}
double fastPower(double x,long long n){if(n<0)return 1.0/fastPower(x,-n);double ans=1;while(n){if(n&1)ans*=x;x*=x;n>>=1;}return ans;}

// 7. Meet in the middle: closest subset sum to target
vector<ll> subsetSums(const vector<int>&a){vector<ll>s{0};for(int x:a){int n=s.size();for(int i=0;i<n;++i)s.push_back(s[i]+x);}return s;}
ll closestSubsetSum(const vector<int>&a,ll goal){int m=a.size()/2;vector<int>l(a.begin(),a.begin()+m),r(a.begin()+m,a.end());auto x=subsetSums(l),y=subsetSums(r);sort(x.begin(),x.end());ll ans=LLONG_MAX;for(ll z:y){auto it=lower_bound(x.begin(),x.end(),goal-z);if(it!=x.end())ans=min(ans,llabs(z+*it-goal));if(it!=x.begin())ans=min(ans,llabs(z+*prev(it)-goal));}return ans;}

// 8. Sparse table for immutable range minimum query
struct SparseTableMin {
    int n;vector<int> lg;vector<vector<int>> st;
    explicit SparseTableMin(const vector<int>&a):n(a.size()),lg(n+1),st(1,vector<int>(n)){if(!n)return;st[0]=a;for(int i=2;i<=n;++i)lg[i]=lg[i/2]+1;st.resize(lg[n]+1,vector<int>(n));for(int k=1;k<(int)st.size();++k)for(int i=0;i+(1<<k)<=n;++i)st[k][i]=min(st[k-1][i],st[k-1][i+(1<<(k-1))]);}
    int query(int l,int r)const{int k=lg[r-l+1];return min(st[k][l],st[k][r-(1<<k)+1]);}
};

// 9. Mo's algorithm: offline range distinct-count queries
vector<int> moDistinctQueries(const vector<int>&a,const vector<pair<int,int>>&queries){
    int n=a.size(),q=queries.size();if(!q)return {};int block=max(1,(int)sqrt(n));
    vector<int>ids(q);iota(ids.begin(),ids.end(),0);sort(ids.begin(),ids.end(),[&](int i,int j){int bi=queries[i].first/block,bj=queries[j].first/block;if(bi!=bj)return bi<bj;return bi&1?queries[i].second>queries[j].second:queries[i].second<queries[j].second;});
    unordered_map<int,int>freq;int distinct=0,L=0,R=-1;vector<int>ans(q);
    auto add=[&](int i){if(++freq[a[i]]==1)++distinct;};auto rem=[&](int i){if(--freq[a[i]]==0)--distinct;};
    for(int id:ids){auto [l,r]=queries[id];while(L>l)add(--L);while(R<r)add(++R);while(L<l)rem(L++);while(R>r)rem(R--);ans[id]=distinct;}return ans;
}

// Complexity reminders:
// Fenwick update/query O(log n); segment tree O(log n); lazy segment tree O(log n).
// DSU with path compression + union by size: amortized inverse-Ackermann.
// Kruskal O(E log E); merge sort O(n log n); quickselect average O(n).
// Meet-in-middle O(2^(n/2) log 2^(n/2)); sparse table build O(n log n), RMQ O(1).
// Mo's typical movement ~O((N+Q)*sqrt(N)) depending on the add/remove cost.

// GRAPH DSA — COMPLETE REVISION (C++17)
// Based on the uploaded Python graph revision notebook.
// Compile: g++ -std=c++17 -O2 -Wall -Wextra graphs_complete_revision.cpp
// Vertices are 0-indexed. Adapt input/output wrappers to the platform.

#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = (1LL << 60);

// ============================================================
// GRAPH REPRESENTATIONS
// ============================================================
struct Graph {
    int n;
    bool directed;
    vector<vector<int>> adj;
    vector<vector<pair<int,ll>>> weighted;

    Graph(int n, bool directed=false): n(n), directed(directed), adj(n), weighted(n) {}
    void addEdge(int u, int v) {
        adj[u].push_back(v);
        if (!directed) adj[v].push_back(u);
    }
    void addWeightedEdge(int u, int v, ll w) {
        weighted[u].push_back({v,w});
        if (!directed) weighted[v].push_back({u,w});
    }
};

vector<vector<int>> buildAdjMatrix(int n, const vector<pair<int,int>>& edges, bool directed=false) {
    vector<vector<int>> mat(n, vector<int>(n));
    for (auto [u,v] : edges) { mat[u][v]=1; if (!directed) mat[v][u]=1; }
    return mat;
}
vector<vector<pair<int,ll>>> buildWeightedAdj(int n, const vector<tuple<int,int,ll>>& edges, bool directed=false) {
    vector<vector<pair<int,ll>>> adj(n);
    for (auto [u,v,w] : edges) { adj[u].push_back({v,w}); if (!directed) adj[v].push_back({u,w}); }
    return adj;
}

// ============================================================
// BFS / DFS / COMPONENTS
// ============================================================
vector<int> bfs(const Graph& g, int start) {
    vector<int> vis(g.n), order;
    queue<int> q; q.push(start); vis[start]=1;
    while (!q.empty()) {
        int u=q.front(); q.pop(); order.push_back(u);
        for (int v:g.adj[u]) if (!vis[v]) vis[v]=1, q.push(v);
    }
    return order;
}
vector<int> bfsDistances(const Graph& g, int start) {
    vector<int> d(g.n,-1); queue<int> q; q.push(start); d[start]=0;
    while (!q.empty()) { int u=q.front(); q.pop(); for(int v:g.adj[u]) if(d[v]==-1) d[v]=d[u]+1,q.push(v); }
    return d;
}
vector<int> bfsPath(const Graph& g, int s, int t) {
    vector<int> par(g.n,-1), d(g.n,-1); queue<int> q; q.push(s); d[s]=0;
    while(!q.empty()) { int u=q.front();q.pop(); if(u==t) break;
        for(int v:g.adj[u]) if(d[v]==-1) d[v]=d[u]+1,par[v]=u,q.push(v);
    }
    if(d[t]==-1) return {};
    vector<int> path; for(int x=t;x!=-1;x=par[x]) path.push_back(x);
    reverse(path.begin(),path.end()); return path;
}
vector<int> dfsRecursive(const Graph& g,int s) {
    vector<int> vis(g.n),out;
    function<void(int)> dfs=[&](int u){vis[u]=1;out.push_back(u);for(int v:g.adj[u])if(!vis[v])dfs(v);};
    dfs(s); return out;
}
vector<int> dfsIterative(const Graph& g,int s) {
    vector<int> vis(g.n),out; stack<int> st;st.push(s);
    while(!st.empty()){int u=st.top();st.pop();if(vis[u])continue;vis[u]=1;out.push_back(u);
        for(auto it=g.adj[u].rbegin();it!=g.adj[u].rend();++it)if(!vis[*it])st.push(*it);}
    return out;
}
vector<vector<int>> connectedComponents(const Graph& g) {
    vector<int> vis(g.n); vector<vector<int>> comps;
    for(int s=0;s<g.n;++s)if(!vis[s]){vector<int> c;stack<int> st;st.push(s);vis[s]=1;
        while(!st.empty()){int u=st.top();st.pop();c.push_back(u);for(int v:g.adj[u])if(!vis[v])vis[v]=1,st.push(v);}
        comps.push_back(c);}
    return comps;
}
int countComponents(const Graph& g){return (int)connectedComponents(g).size();}

// ============================================================
// CYCLE DETECTION
// ============================================================
bool hasUndirectedCycleDFS(const Graph& g) {
    vector<int> vis(g.n);
    function<bool(int,int)> dfs=[&](int u,int p){vis[u]=1;for(int v:g.adj[u]){
        if(!vis[v]){if(dfs(v,u))return true;} else if(v!=p)return true;}return false;};
    for(int i=0;i<g.n;++i)if(!vis[i]&&dfs(i,-1))return true;return false;
}
bool hasUndirectedCycleBFS(const Graph& g) {
    vector<int> vis(g.n);
    for(int s=0;s<g.n;++s)if(!vis[s]){queue<pair<int,int>>q;q.push({s,-1});vis[s]=1;
        while(!q.empty()){auto [u,p]=q.front();q.pop();for(int v:g.adj[u]){
            if(!vis[v])vis[v]=1,q.push({v,u});else if(v!=p)return true;}}}
    return false;
}
bool hasDirectedCycle(const Graph& g) {
    vector<int> state(g.n); // 0=unseen, 1=active, 2=done
    function<bool(int)> dfs=[&](int u){state[u]=1;for(int v:g.adj[u]){
        if(state[v]==1)return true;if(state[v]==0&&dfs(v))return true;}state[u]=2;return false;};
    for(int i=0;i<g.n;++i)if(!state[i]&&dfs(i))return true;return false;
}
bool isBipartite(const Graph& g) {
    vector<int> color(g.n,-1);
    for(int s=0;s<g.n;++s)if(color[s]==-1){queue<int>q;q.push(s);color[s]=0;
        while(!q.empty()){int u=q.front();q.pop();for(int v:g.adj[u]){
            if(color[v]==-1)color[v]=1-color[u],q.push(v);else if(color[v]==color[u])return false;}}}
    return true;
}

// ============================================================
// TOPOLOGICAL SORT / COURSE SCHEDULE
// ============================================================
vector<int> topoKahn(const Graph& g) {
    vector<int> indeg(g.n),order;for(int u=0;u<g.n;++u)for(int v:g.adj[u])++indeg[v];
    queue<int>q;for(int i=0;i<g.n;++i)if(!indeg[i])q.push(i);
    while(!q.empty()){int u=q.front();q.pop();order.push_back(u);for(int v:g.adj[u])if(--indeg[v]==0)q.push(v);}
    if((int)order.size()!=g.n)return {};return order;
}
vector<int> topoDFS(const Graph& g) {
    vector<int> state(g.n),order;
    function<bool(int)> dfs=[&](int u){state[u]=1;for(int v:g.adj[u]){
        if(state[v]==1)return false;if(state[v]==0&&!dfs(v))return false;}state[u]=2;order.push_back(u);return true;};
    for(int i=0;i<g.n;++i)if(!state[i]&&!dfs(i))return {};
    reverse(order.begin(),order.end());return order;
}
bool canFinishCourses(int n,const vector<pair<int,int>>& prerequisites) {
    Graph g(n,true);for(auto [course,pre]:prerequisites)g.addEdge(pre,course);return (int)topoKahn(g).size()==n;
}
vector<int> courseOrder(int n,const vector<pair<int,int>>& prerequisites) {
    Graph g(n,true);for(auto [course,pre]:prerequisites)g.addEdge(pre,course);return topoKahn(g);
}

// ============================================================
// SHORTEST PATHS: DIJKSTRA, BELLMAN-FORD, FLOYD-WARSHALL, 0-1 BFS
// ============================================================
vector<ll> dijkstra(const Graph& g,int source) { // nonnegative weights only
    vector<ll>d(g.n,INF);priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<>>pq;d[source]=0;pq.push({0,source});
    while(!pq.empty()){auto [du,u]=pq.top();pq.pop();if(du!=d[u])continue;
        for(auto [v,w]:g.weighted[u])if(du+w<d[v])d[v]=du+w,pq.push({d[v],v});}
    return d;
}
pair<vector<ll>,vector<int>> dijkstraParent(const Graph& g,int s) {
    vector<ll>d(g.n,INF);vector<int>par(g.n,-1);priority_queue<pair<ll,int>,vector<pair<ll,int>>,greater<>>pq;d[s]=0;pq.push({0,s});
    while(!pq.empty()){auto [du,u]=pq.top();pq.pop();if(du!=d[u])continue;
        for(auto [v,w]:g.weighted[u])if(du+w<d[v])d[v]=du+w,par[v]=u,pq.push({d[v],v});}
    return {d,par};
}
vector<int> reconstructPath(const vector<int>& par,int s,int t) {
    vector<int>p;if(t!=s&&par[t]==-1)return {};
    for(int x=t;x!=-1;x=par[x]){p.push_back(x);if(x==s)break;}
    if(p.back()!=s)return {};reverse(p.begin(),p.end());return p;
}
pair<vector<ll>,bool> bellmanFord(int n,const vector<tuple<int,int,ll>>& edges,int source) {
    vector<ll>d(n,INF);d[source]=0;
    for(int i=0;i<n-1;++i){bool changed=false;for(auto [u,v,w]:edges)if(d[u]!=INF&&d[u]+w<d[v])d[v]=d[u]+w,changed=true;if(!changed)break;}
    bool neg=false;for(auto [u,v,w]:edges)if(d[u]!=INF&&d[u]+w<d[v]){neg=true;break;}
    return {d,neg};
}
vector<vector<ll>> floydWarshall(int n,const vector<tuple<int,int,ll>>& edges,bool directed=true) {
    vector<vector<ll>>d(n,vector<ll>(n,INF));for(int i=0;i<n;++i)d[i][i]=0;
    for(auto [u,v,w]:edges){d[u][v]=min(d[u][v],w);if(!directed)d[v][u]=min(d[v][u],w);}
    for(int k=0;k<n;++k)for(int i=0;i<n;++i)if(d[i][k]!=INF)for(int j=0;j<n;++j)if(d[k][j]!=INF)
        d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
    return d;
}
bool hasNegativeCycleFW(const vector<vector<ll>>& d){for(int i=0;i<(int)d.size();++i)if(d[i][i]<0)return true;return false;}
vector<int> zeroOneBFS(const Graph& g,int source) {
    vector<int>d(g.n,INT_MAX);deque<int>q;d[source]=0;q.push_front(source);
    while(!q.empty()){int u=q.front();q.pop_front();for(auto [v,w]:g.weighted[u]){
        int nd=d[u]+(int)w;if(nd<d[v]){d[v]=nd;if(w==0)q.push_front(v);else q.push_back(v);}}}
    return d;
}

// ============================================================
// DISJOINT SET UNION / UNION-FIND
// ============================================================
struct DSU {
    vector<int> parent,rankv,size;
    DSU(int n):parent(n),rankv(n),size(n,1){iota(parent.begin(),parent.end(),0);}
    int find(int x){return parent[x]==x?x:parent[x]=find(parent[x]);}
    bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(rankv[a]<rankv[b])swap(a,b);
        parent[b]=a;if(rankv[a]==rankv[b])++rankv[a];return true;}
    bool uniteBySize(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(size[a]<size[b])swap(a,b);
        parent[b]=a;size[a]+=size[b];return true;}
    bool connected(int a,int b){return find(a)==find(b);}
};
bool hasCycleDSU(int n,const vector<pair<int,int>>& edges){DSU d(n);for(auto [u,v]:edges)if(!d.unite(u,v))return true;return false;}

// ============================================================
// MINIMUM SPANNING TREE: KRUSKAL / PRIM
// ============================================================
pair<ll,vector<tuple<int,int,ll>>> kruskalMST(int n,vector<tuple<int,int,ll>> edges) {
    sort(edges.begin(),edges.end(),[](auto&a,auto&b){return get<2>(a)<get<2>(b);});
    DSU d(n);ll total=0;vector<tuple<int,int,ll>>mst;
    for(auto [u,v,w]:edges)if(d.unite(u,v)){mst.push_back({u,v,w});total+=w;if((int)mst.size()==n-1)break;}
    return {total,mst}; // fewer than n-1 edges means disconnected graph
}
pair<ll,vector<tuple<int,int,ll>>> primMST(const Graph& g) { // undirected weighted graph
    if(!g.n)return {0,{}};vector<int>vis(g.n);using T=tuple<ll,int,int>;
    priority_queue<T,vector<T>,greater<>>pq;pq.push({0,0,-1});ll total=0;vector<tuple<int,int,ll>>mst;
    while(!pq.empty()){auto [w,u,p]=pq.top();pq.pop();if(vis[u])continue;vis[u]=1;total+=w;if(p!=-1)mst.push_back({p,u,w});
        for(auto [v,c]:g.weighted[u])if(!vis[v])pq.push({c,v,u});}
    return {total,mst};
}

// ============================================================
// GRID DFS / BFS PATTERNS
// ============================================================
const int DR[4]={-1,1,0,0}, DC[4]={0,0,-1,1};
int countIslands(vector<vector<char>> grid) {
    if(grid.empty())return 0;int R=grid.size(),C=grid[0].size(),cnt=0;
    function<void(int,int)>dfs=[&](int r,int c){if(r<0||r>=R||c<0||c>=C||grid[r][c]!='1')return;
        grid[r][c]='0';for(int k=0;k<4;++k)dfs(r+DR[k],c+DC[k]);};
    for(int r=0;r<R;++r)for(int c=0;c<C;++c)if(grid[r][c]=='1')++cnt,dfs(r,c);return cnt;
}
vector<vector<int>> floodFill(vector<vector<int>> image,int sr,int sc,int color) {
    int R=image.size(),C=image[0].size(),old=image[sr][sc];if(old==color)return image;
    function<void(int,int)>dfs=[&](int r,int c){if(r<0||r>=R||c<0||c>=C||image[r][c]!=old)return;
        image[r][c]=color;for(int k=0;k<4;++k)dfs(r+DR[k],c+DC[k]);};dfs(sr,sc);return image;
}
int shortestPathBinaryGrid(const vector<vector<int>>&grid) { // 0=open, 1=blocked; length counts cells
    if(grid.empty()||grid[0].empty()||grid[0][0])return -1;int R=grid.size(),C=grid[0].size();
    vector<vector<int>>d(R,vector<int>(C,-1));queue<pair<int,int>>q;q.push({0,0});d[0][0]=1;
    while(!q.empty()){auto [r,c]=q.front();q.pop();if(r==R-1&&c==C-1)return d[r][c];
        for(int k=0;k<4;++k){int nr=r+DR[k],nc=c+DC[k];if(nr>=0&&nr<R&&nc>=0&&nc<C&&!grid[nr][nc]&&d[nr][nc]==-1)d[nr][nc]=d[r][c]+1,q.push({nr,nc});}}
    return -1;
}
int rottenOranges(vector<vector<int>>&grid) {
    if(grid.empty())return 0;int R=grid.size(),C=grid[0].size(),fresh=0,minutes=0;queue<pair<int,int>>q;
    for(int r=0;r<R;++r)for(int c=0;c<C;++c)if(grid[r][c]==2)q.push({r,c});else if(grid[r][c]==1)++fresh;
    while(!q.empty()&&fresh){int sz=q.size();while(sz--){auto [r,c]=q.front();q.pop();for(int k=0;k<4;++k){int nr=r+DR[k],nc=c+DC[k];
        if(nr>=0&&nr<R&&nc>=0&&nc<C&&grid[nr][nc]==1)grid[nr][nc]=2,--fresh,q.push({nr,nc});}}++minutes;}
    return fresh?-1:minutes;
}

// ============================================================
// STRONGLY CONNECTED COMPONENTS: KOSARAJU / TARJAN
// ============================================================
vector<vector<int>> kosarajuSCC(const Graph&g) {
    vector<int>vis(g.n),order;function<void(int)>dfs1=[&](int u){vis[u]=1;for(int v:g.adj[u])if(!vis[v])dfs1(v);order.push_back(u);};
    for(int i=0;i<g.n;++i)if(!vis[i])dfs1(i);
    vector<vector<int>>rev(g.n);for(int u=0;u<g.n;++u)for(int v:g.adj[u])rev[v].push_back(u);
    fill(vis.begin(),vis.end(),0);vector<vector<int>>comps;
    function<void(int,vector<int>&)>dfs2=[&](int u,vector<int>&c){vis[u]=1;c.push_back(u);for(int v:rev[u])if(!vis[v])dfs2(v,c);};
    for(auto it=order.rbegin();it!=order.rend();++it)if(!vis[*it]){vector<int>c;dfs2(*it,c);comps.push_back(c);}return comps;
}
vector<vector<int>> tarjanSCC(const Graph&g) {
    int timer=0;vector<int>disc(g.n,-1),low(g.n),on(g.n),st;vector<vector<int>>comps;
    function<void(int)>dfs=[&](int u){disc[u]=low[u]=timer++;st.push_back(u);on[u]=1;
        for(int v:g.adj[u])if(disc[v]==-1){dfs(v);low[u]=min(low[u],low[v]);}else if(on[v])low[u]=min(low[u],disc[v]);
        if(low[u]==disc[u]){vector<int>c;while(true){int x=st.back();st.pop_back();on[x]=0;c.push_back(x);if(x==u)break;}comps.push_back(c);}};
    for(int i=0;i<g.n;++i)if(disc[i]==-1)dfs(i);return comps;
}

// ============================================================
// BRIDGES / ARTICULATION POINTS (undirected; simple graph assumptions)
// ============================================================
vector<pair<int,int>> findBridges(const Graph&g) {
    int timer=0;vector<int>disc(g.n,-1),low(g.n);vector<pair<int,int>>ans;
    function<void(int,int)>dfs=[&](int u,int p){disc[u]=low[u]=timer++;for(int v:g.adj[u]){if(v==p)continue;
        if(disc[v]==-1){dfs(v,u);low[u]=min(low[u],low[v]);if(low[v]>disc[u])ans.push_back({u,v});}
        else low[u]=min(low[u],disc[v]);}};
    for(int i=0;i<g.n;++i)if(disc[i]==-1)dfs(i,-1);return ans;
}
vector<int> articulationPoints(const Graph&g) {
    int timer=0;vector<int>disc(g.n,-1),low(g.n);set<int>ans;
    function<void(int,int)>dfs=[&](int u,int p){disc[u]=low[u]=timer++;int children=0;
        for(int v:g.adj[u]){if(v==p)continue;if(disc[v]==-1){++children;dfs(v,u);low[u]=min(low[u],low[v]);
            if(p!=-1&&low[v]>=disc[u])ans.insert(u);}else low[u]=min(low[u],disc[v]);}
        if(p==-1&&children>1)ans.insert(u);};
    for(int i=0;i<g.n;++i)if(disc[i]==-1)dfs(i,-1);return {ans.begin(),ans.end()};
}

// ============================================================
// GRAPH CLONING
// ============================================================
struct GraphNode { int val; vector<GraphNode*> neighbors; explicit GraphNode(int x):val(x){} };
GraphNode* cloneGraph(GraphNode* node) {
    if(!node)return nullptr;unordered_map<GraphNode*,GraphNode*>copies;
    function<GraphNode*(GraphNode*)>dfs=[&](GraphNode*cur)->GraphNode*{
        if(copies.count(cur))return copies[cur];auto*copy=new GraphNode(cur->val);copies[cur]=copy;
        for(auto*n:cur->neighbors)copy->neighbors.push_back(dfs(n));return copy;};
    return dfs(node);
}

// ============================================================
// WORD LADDER (BFS)
// ============================================================
int wordLadderLength(string beginWord,string endWord,vector<string>wordList) {
    unordered_set<string>dict(wordList.begin(),wordList.end());if(!dict.count(endWord))return 0;
    queue<pair<string,int>>q;q.push({beginWord,1});unordered_set<string>vis{beginWord};
    while(!q.empty()){auto [word,depth]=q.front();q.pop();if(word==endWord)return depth;
        for(int i=0;i<(int)word.size();++i){char old=word[i];for(char c='a';c<='z';++c){word[i]=c;
            if(dict.count(word)&&!vis.count(word))vis.insert(word),q.push({word,depth+1});}word[i]=old;}}
    return 0;
}

// ============================================================
// QUICK COMPLEXITY REMINDERS
// BFS/DFS: O(V+E); Dijkstra: O((V+E)logV); Bellman-Ford: O(VE)
// Floyd-Warshall: O(V^3); DSU amortized ~O(1); Kruskal: O(ElogE)
// MST: spanning tree exists only if graph is connected.
// Dijkstra requires nonnegative weights. Topological order requires a DAG.
// ============================================================

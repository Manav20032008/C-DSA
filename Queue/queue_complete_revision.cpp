/*
QUEUE — COMPLETE C++17 REVISION CODEBOOK
=======================================
FIFO fundamentals; array/circular/linked queue; deque; priority queues;
queue/stack conversions; graph and grid BFS; binary-tree BFS views;
monotonic sliding windows; Josephus; round-robin; Kahn topological sort;
0-1 BFS; queue operations; heap patterns; Word Ladder.
Compile: g++ -std=c++17 -O2 -Wall -Wextra queue_complete_revision.cpp
*/
#include <bits/stdc++.h>
using namespace std;

// Queue: FIFO. enqueue/push_back and dequeue/pop_front are O(1) with deque.
class SimpleQueue {
    vector<int> a; size_t head=0;
public:
    void enqueue(int x){a.push_back(x);}
    int dequeue(){if(empty()) throw underflow_error("Queue empty"); int x=a[head++]; if(head>100 && head*2>a.size()){a.erase(a.begin(),a.begin()+head);head=0;} return x;}
    int front() const {if(empty()) throw underflow_error("Queue empty");return a[head];}
    int rear() const {if(empty()) throw underflow_error("Queue empty");return a.back();}
    bool empty() const{return head>=a.size();} size_t size() const{return a.size()-head;}
};
class LinkedQueue {
    struct Node{int val;Node* next=nullptr;explicit Node(int x):val(x){}};
    Node *f=nullptr,*r=nullptr; size_t n=0;
public:
    ~LinkedQueue(){while(f){Node*t=f;f=f->next;delete t;}}
    void enqueue(int x){Node*t=new Node(x);if(!r)f=r=t;else r->next=t,r=t;++n;}
    int dequeue(){if(!f)throw underflow_error("Queue empty");Node*t=f;int x=t->val;f=f->next;if(!f)r=nullptr;delete t;--n;return x;}
    int front()const{if(!f)throw underflow_error("Queue empty");return f->val;}
    int rear()const{if(!r)throw underflow_error("Queue empty");return r->val;}
    bool empty()const{return !f;}size_t size()const{return n;}
};
class CircularQueue {
    vector<int>a;size_t f=0,r=0,n=0;
public:
    explicit CircularQueue(size_t cap):a(cap){if(!cap)throw invalid_argument("Capacity must be positive");}
    bool empty()const{return n==0;}bool full()const{return n==a.size();}size_t size()const{return n;}
    void enqueue(int x){if(full())throw overflow_error("Queue full");a[r]=x;r=(r+1)%a.size();++n;}
    int dequeue(){if(empty())throw underflow_error("Queue empty");int x=a[f];f=(f+1)%a.size();--n;return x;}
    int front()const{if(empty())throw underflow_error("Queue empty");return a[f];}
    int rear()const{if(empty())throw underflow_error("Queue empty");return a[(r+a.size()-1)%a.size()];}
};
using Deque=deque<int>;
class MinPriorityQueue {priority_queue<int,vector<int>,greater<int>>q;public:void push(int x){q.push(x);}int pop(){if(q.empty())throw underflow_error("Empty heap");int x=q.top();q.pop();return x;}int peek()const{if(q.empty())throw underflow_error("Empty heap");return q.top();}bool empty()const{return q.empty();}};
class MaxPriorityQueue {priority_queue<int>q;public:void push(int x){q.push(x);}int pop(){if(q.empty())throw underflow_error("Empty heap");int x=q.top();q.pop();return x;}int peek()const{if(q.empty())throw underflow_error("Empty heap");return q.top();}bool empty()const{return q.empty();}};
// Stable task priority: smaller priority number comes first; FIFO for ties.
class TaskPriorityQueue {using Item=tuple<int,long long,string>;priority_queue<Item,vector<Item>,greater<Item>>q;long long seq=0;public:void push(int p,string task){q.emplace(p,seq++,move(task));}string pop(){if(q.empty())throw underflow_error("Empty heap");auto [p,s,t]=q.top();q.pop();return t;}};
class QueueUsingTwoStacks {stack<int>in,out;void transfer(){if(out.empty())while(!in.empty())out.push(in.top()),in.pop();}public:void enqueue(int x){in.push(x);}int dequeue(){transfer();if(out.empty())throw underflow_error("Queue empty");int x=out.top();out.pop();return x;}int peek(){transfer();if(out.empty())throw underflow_error("Queue empty");return out.top();}bool empty()const{return in.empty()&&out.empty();}};
class StackUsingTwoQueues {queue<int>q;public:void push(int x){q.push(x);for(size_t i=1;i<q.size();++i)q.push(q.front()),q.pop();}int pop(){if(q.empty())throw underflow_error("Stack empty");int x=q.front();q.pop();return x;}int top()const{if(q.empty())throw underflow_error("Stack empty");return q.front();}bool empty()const{return q.empty();}};

vector<int> bfsGraph(const vector<vector<int>>&g,int s){vector<int>order,vis(g.size());queue<int>q;if(s<0||s>=(int)g.size())return order;vis[s]=1;q.push(s);while(!q.empty()){int u=q.front();q.pop();order.push_back(u);for(int v:g[u])if(!vis[v])vis[v]=1,q.push(v);}return order;}
int shortestUnweighted(const vector<vector<int>>&g,int s,int t){vector<int>d(g.size(),-1);queue<int>q;d[s]=0;q.push(s);while(!q.empty()){int u=q.front();q.pop();if(u==t)return d[u];for(int v:g[u])if(d[v]<0)d[v]=d[u]+1,q.push(v);}return -1;}
vector<int> shortestPath(const vector<vector<int>>&g,int s,int t){vector<int>p(g.size(),-1);queue<int>q;p[s]=s;q.push(s);while(!q.empty()){int u=q.front();q.pop();if(u==t)break;for(int v:g[u])if(p[v]<0)p[v]=u,q.push(v);}if(p[t]<0)return {};vector<int>path;for(int x=t;x!=s;x=p[x])path.push_back(x);path.push_back(s);reverse(path.begin(),path.end());return path;}
int countComponents(const vector<vector<int>>&g){vector<char>v(g.size());int c=0;for(int s=0;s<(int)g.size();++s)if(!v[s]){++c;queue<int>q;q.push(s);v[s]=1;while(!q.empty()){int u=q.front();q.pop();for(int w:g[u])if(!v[w])v[w]=1,q.push(w);}}return c;}
struct TreeNode{int val;TreeNode*left=nullptr,*right=nullptr;explicit TreeNode(int x):val(x){}};
vector<vector<int>> levelOrder(TreeNode*r){vector<vector<int>>a;if(!r)return a;queue<TreeNode*>q;q.push(r);while(!q.empty()){int n=q.size();vector<int>lev;while(n--){auto*u=q.front();q.pop();lev.push_back(u->val);if(u->left)q.push(u->left);if(u->right)q.push(u->right);}a.push_back(move(lev));}return a;}
vector<int> rightView(TreeNode*r){vector<int>a;if(!r)return a;queue<TreeNode*>q;q.push(r);while(!q.empty()){int n=q.size();for(int i=0;i<n;++i){auto*u=q.front();q.pop();if(i==n-1)a.push_back(u->val);if(u->left)q.push(u->left);if(u->right)q.push(u->right);}}return a;}
vector<int> leftView(TreeNode*r){vector<int>a;if(!r)return a;queue<TreeNode*>q;q.push(r);while(!q.empty()){int n=q.size();for(int i=0;i<n;++i){auto*u=q.front();q.pop();if(!i)a.push_back(u->val);if(u->left)q.push(u->left);if(u->right)q.push(u->right);}}return a;}
vector<double> averageLevels(TreeNode*r){vector<double>a;if(!r)return a;queue<TreeNode*>q;q.push(r);while(!q.empty()){int n=q.size();long long s=0;for(int i=0;i<n;++i){auto*u=q.front();q.pop();s+=u->val;if(u->left)q.push(u->left);if(u->right)q.push(u->right);}a.push_back((double)s/n);}return a;}
int minDepth(TreeNode*r){if(!r)return 0;queue<pair<TreeNode*,int>>q;q.push({r,1});while(!q.empty()){auto [u,d]=q.front();q.pop();if(!u->left&&!u->right)return d;if(u->left)q.push({u->left,d+1});if(u->right)q.push({u->right,d+1});}return 0;}
int orangesRotting(vector<vector<int>>&g){int m=g.size();if(!m)return 0;int n=g[0].size(),fresh=0,t=0;queue<pair<int,int>>q;for(int i=0;i<m;++i)for(int j=0;j<n;++j)if(g[i][j]==2)q.push({i,j});else if(g[i][j]==1)++fresh;int dr[]={1,-1,0,0},dc[]={0,0,1,-1};while(!q.empty()&&fresh){int z=q.size();++t;while(z--){auto [r,c]=q.front();q.pop();for(int k=0;k<4;++k){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<m&&y>=0&&y<n&&g[x][y]==1)g[x][y]=2,--fresh,q.push({x,y});}}}return fresh?-1:t;}
int numIslandsBFS(vector<vector<char>>&g){int m=g.size();if(!m)return 0;int n=g[0].size(),ans=0,dr[]={1,-1,0,0},dc[]={0,0,1,-1};for(int i=0;i<m;++i)for(int j=0;j<n;++j)if(g[i][j]=='1'){++ans;queue<pair<int,int>>q;q.push({i,j});g[i][j]='0';while(!q.empty()){auto [r,c]=q.front();q.pop();for(int k=0;k<4;++k){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<m&&y>=0&&y<n&&g[x][y]=='1')g[x][y]='0',q.push({x,y});}}}return ans;}
vector<vector<int>> floodFill(vector<vector<int>>im,int sr,int sc,int color){int old=im[sr][sc];if(old==color)return im;int m=im.size(),n=im[0].size(),dr[]={1,-1,0,0},dc[]={0,0,1,-1};queue<pair<int,int>>q;q.push({sr,sc});im[sr][sc]=color;while(!q.empty()){auto [r,c]=q.front();q.pop();for(int k=0;k<4;++k){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<m&&y>=0&&y<n&&im[x][y]==old)im[x][y]=color,q.push({x,y});}}return im;}
vector<int> maxSlidingWindow(const vector<int>&a,int k){if(k<=0||k>(int)a.size())return {};deque<int>q;vector<int>r;for(int i=0;i<(int)a.size();++i){while(!q.empty()&&q.front()<=i-k)q.pop_front();while(!q.empty()&&a[q.back()]<=a[i])q.pop_back();q.push_back(i);if(i>=k-1)r.push_back(a[q.front()]);}return r;}
vector<int> minSlidingWindow(const vector<int>&a,int k){if(k<=0||k>(int)a.size())return {};deque<int>q;vector<int>r;for(int i=0;i<(int)a.size();++i){while(!q.empty()&&q.front()<=i-k)q.pop_front();while(!q.empty()&&a[q.back()]>=a[i])q.pop_back();q.push_back(i);if(i>=k-1)r.push_back(a[q.front()]);}return r;}
vector<int> firstNegativeWindow(const vector<int>&a,int k){vector<int>r;if(k<=0||k>(int)a.size())return r;deque<int>q;for(int i=0;i<(int)a.size();++i){if(a[i]<0)q.push_back(i);while(!q.empty()&&q.front()<=i-k)q.pop_front();if(i>=k-1)r.push_back(q.empty()?0:a[q.front()]);}return r;}
vector<char> firstNonRepeatingStream(const string&s){int cnt[256]={};queue<char>q;vector<char>ans;for(unsigned char c:s){++cnt[c];q.push(c);while(!q.empty()&&cnt[(unsigned char)q.front()]>1)q.pop();ans.push_back(q.empty()?'#':q.front());}return ans;}
vector<string> generateBinary(int n){vector<string>a;if(n<=0)return a;queue<string>q;q.push("1");while(n--){string s=q.front();q.pop();a.push_back(s);q.push(s+"0");q.push(s+"1");}return a;}
int josephus(int n,int k){if(n<=0||k<=0)return -1;queue<int>q;for(int i=1;i<=n;++i)q.push(i);while(q.size()>1){for(int i=1;i<k;++i)q.push(q.front()),q.pop();q.pop();}return q.front();}
int josephusMath(int n,int k){int r=0;for(int i=1;i<=n;++i)r=(r+k)%i;return n>0&&k>0?r+1:-1;}
vector<pair<int,int>> roundRobin(vector<int>tasks,int quantum){vector<pair<int,int>>done;if(quantum<=0)return done;queue<pair<int,int>>q;for(int i=0;i<(int)tasks.size();++i)if(tasks[i]>0)q.push({i,tasks[i]});while(!q.empty()){auto [id,rem]=q.front();q.pop();int used=min(quantum,rem);done.push_back({id,used});rem-=used;if(rem)q.push({id,rem});}return done;}
vector<int> topoKahn(int n,const vector<pair<int,int>>&edges){vector<vector<int>>g(n);vector<int>in(n);for(auto [u,v]:edges)g[u].push_back(v),++in[v];queue<int>q;for(int i=0;i<n;++i)if(!in[i])q.push(i);vector<int>o;while(!q.empty()){int u=q.front();q.pop();o.push_back(u);for(int v:g[u])if(--in[v]==0)q.push(v);}if((int)o.size()!=n)return {};return o;}
bool canFinish(int n,const vector<pair<int,int>>&pre){return (int)topoKahn(n,pre).size()==n;}
vector<int> zeroOneBFS(const vector<vector<pair<int,int>>>&g,int s){const int INF=1e9;vector<int>d(g.size(),INF);deque<int>q;d[s]=0;q.push_front(s);while(!q.empty()){int u=q.front();q.pop_front();for(auto [v,w]:g[u])if(d[v]>d[u]+w){d[v]=d[u]+w;if(w==0)q.push_front(v);else q.push_back(v);}}return d;}
int shortestPathGrid(const vector<vector<int>>&g,pair<int,int>s,pair<int,int>t){int m=g.size();if(!m)return -1;int n=g[0].size();if(g[s.first][s.second]||g[t.first][t.second])return -1;vector<vector<int>>d(m,vector<int>(n,-1));queue<pair<int,int>>q;q.push(s);d[s.first][s.second]=0;int dr[]={1,-1,0,0},dc[]={0,0,1,-1};while(!q.empty()){auto [r,c]=q.front();q.pop();if(make_pair(r,c)==t)return d[r][c];for(int k=0;k<4;++k){int x=r+dr[k],y=c+dc[k];if(x>=0&&x<m&&y>=0&&y<n&&!g[x][y]&&d[x][y]<0)d[x][y]=d[r][c]+1,q.push({x,y});}}return -1;}
// Queue reversal helpers (operate on std::queue).
void reverseQueue(queue<int>&q){stack<int>s;while(!q.empty())s.push(q.front()),q.pop();while(!s.empty())q.push(s.top()),s.pop();}
void reverseFirstK(queue<int>&q,int k){if(k<0||k>(int)q.size())return;stack<int>s;for(int i=0;i<k;++i)s.push(q.front()),q.pop();while(!s.empty())q.push(s.top()),s.pop();int rest=q.size()-k;while(rest--)q.push(q.front()),q.pop();}
void interleaveQueue(queue<int>&q){int n=q.size();if(n%2)return;queue<int>a;for(int i=0;i<n/2;++i)a.push(q.front()),q.pop();while(!a.empty()){q.push(a.front());a.pop();q.push(q.front());q.pop();}}
bool isQueueSorted(queue<int>q){if(q.empty())return true;int prev=q.front();q.pop();while(!q.empty()){if(q.front()<prev)return false;prev=q.front();q.pop();}return true;}
int kthLargest(vector<int>a,int k){if(k<1||k>(int)a.size())return -1;priority_queue<int,vector<int>,greater<int>>q;for(int x:a){q.push(x);if((int)q.size()>k)q.pop();}return q.top();}
vector<int> mergeKSortedArrays(const vector<vector<int>>&a){using T=tuple<int,int,int>;priority_queue<T,vector<T>,greater<T>>q;for(int i=0;i<(int)a.size();++i)if(!a[i].empty())q.emplace(a[i][0],i,0);vector<int>r;while(!q.empty()){auto [x,i,j]=q.top();q.pop();r.push_back(x);if(j+1<(int)a[i].size())q.emplace(a[i][j+1],i,j+1);}return r;}
vector<vector<int>> kClosestPoints(const vector<vector<int>>&p,int k){priority_queue<pair<long long,int>>q;for(int i=0;i<(int)p.size();++i){long long d=1LL*p[i][0]*p[i][0]+1LL*p[i][1]*p[i][1];q.push({d,i});if((int)q.size()>k)q.pop();}vector<vector<int>>r;while(!q.empty()){r.push_back(p[q.top().second]);q.pop();}return r;}
int taskScheduler(vector<char>tasks,int cooldown){vector<int>f(256);for(unsigned char c:tasks)++f[c];priority_queue<int>q;for(int x:f)if(x)q.push(x);int time=0;while(!q.empty()){int cycle=cooldown+1,used=0;vector<int>tmp;while(cycle--&&!q.empty()){int x=q.top();q.pop();if(--x)tmp.push_back(x);++used;++time;}for(int x:tmp)q.push(x);if(q.empty())break;time+=cycle+1;}return time;}
int wordLadderLength(string begin,string end,vector<string>words){unordered_set<string>dict(words.begin(),words.end());if(!dict.count(end))return 0;queue<pair<string,int>>q;q.push({begin,1});unordered_set<string>vis{begin};while(!q.empty()){auto [s,d]=q.front();q.pop();if(s==end)return d;for(int i=0;i<(int)s.size();++i){char old=s[i];for(char c='a';c<='z';++c){s[i]=c;if(dict.count(s)&&!vis.count(s))vis.insert(s),q.push({s,d+1});}s[i]=old;}}return 0;}

#ifdef RUN_REVISION_TESTS
int main(){assert((maxSlidingWindow({1,3,-1,-3,5,3,6,7},3)==vector<int>{3,3,5,5,6,7}));assert(josephus(5,2)==3);assert((topoKahn(4,{{0,1},{0,2},{1,3},{2,3}}).size()==4));assert(shortestUnweighted({{1},{0,2},{1}},0,2)==2);CircularQueue q(2);q.enqueue(1);q.enqueue(2);assert(q.dequeue()==1);q.enqueue(3);assert(q.rear()==3);cout<<"Queue revision tests passed.\\n";}
#endif

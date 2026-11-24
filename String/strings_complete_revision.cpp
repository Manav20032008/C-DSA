// STRING DSA — COMPLETE REVISION (C++17)
// Based on the uploaded Python string revision notebook.
// Compile: g++ -std=c++17 -O2 -Wall -Wextra strings_complete_revision.cpp
// Most examples use std::string (byte/ASCII-oriented unless noted).

#include <bits/stdc++.h>
using namespace std;

// ============================================================
// BASIC OPERATIONS / CHARACTER FREQUENCY
// ============================================================
string reverseString(string s){reverse(s.begin(),s.end());return s;}
vector<int> charFrequency(const string&s){vector<int>f(256);for(unsigned char c:s)++f[c];return f;}
int firstNonRepeatingIndex(const string&s){auto f=charFrequency(s);for(int i=0;i<(int)s.size();++i)if(f[(unsigned char)s[i]]==1)return i;return -1;}
char firstRepeatingCharacter(const string&s){vector<int>f(256);for(unsigned char c:s){if(f[c])return (char)c;f[c]=1;}return '\0';}
string removeWhitespace(const string&s){string out;for(unsigned char c:s)if(!isspace(c))out+=c;return out;}
string toggleCase(string s){for(char&c:s){unsigned char x=c;if(islower(x))c=toupper(x);else if(isupper(x))c=tolower(x);}return s;}
bool isAlphaNumeric(const string&s){for(unsigned char c:s)if(!isalnum(c))return false;return true;}
bool allLowercase(const string&s){for(unsigned char c:s)if(isalpha(c)&&!islower(c))return false;return true;}

// Characters in a that remain after consuming matching character counts from b.
string characterDifference(const string&a,const string&b){array<int,256>f{};for(unsigned char c:b)++f[c];string out;
    for(unsigned char c:a)if(f[c])--f[c];else out+=(char)c;return out;}

// ============================================================
// PALINDROMES
// ============================================================
bool isPalindrome(const string&s){int l=0,r=(int)s.size()-1;while(l<r)if(s[l++]!=s[r--])return false;return true;}
bool isPalindromeIgnoreCaseAlnum(const string&s){int l=0,r=(int)s.size()-1;while(l<r){
    while(l<r&&!isalnum((unsigned char)s[l]))++l;while(l<r&&!isalnum((unsigned char)s[r]))--r;
    if(tolower((unsigned char)s[l])!=tolower((unsigned char)s[r]))return false;++l;--r;}return true;}
bool validPalindromeOneDeletion(const string&s){auto check=[&](int l,int r){while(l<r)if(s[l++]!=s[r--])return false;return true;};
    int l=0,r=(int)s.size()-1;while(l<r){if(s[l]!=s[r])return check(l+1,r)||check(l,r-1);++l;--r;}return true;}
string longestPalindromicSubstring(const string&s){if(s.empty())return "";int bestL=0,bestR=0;
    auto expand=[&](int l,int r){while(l>=0&&r<(int)s.size()&&s[l]==s[r]){if(r-l>bestR-bestL)bestL=l,bestR=r;--l;++r;}};
    for(int i=0;i<(int)s.size();++i){expand(i,i);expand(i,i+1);}return s.substr(bestL,bestR-bestL+1);}
int countPalindromicSubstrings(const string&s){int count=0;auto expand=[&](int l,int r){while(l>=0&&r<(int)s.size()&&s[l]==s[r])++count,--l,++r;};
    for(int i=0;i<(int)s.size();++i){expand(i,i);expand(i,i+1);}return count;}

// ============================================================
// ANAGRAMS / WINDOW MATCHES
// ============================================================
bool areAnagrams(const string&a,const string&b){if(a.size()!=b.size())return false;array<int,256>f{};for(unsigned char c:a)++f[c];for(unsigned char c:b)if(--f[c]<0)return false;return true;}
vector<vector<string>> groupAnagrams(const vector<string>&words){unordered_map<string,vector<string>>groups;
    for(auto w:words){string key=w;sort(key.begin(),key.end());groups[key].push_back(w);}vector<vector<string>>out;
    for(auto&[k,v]:groups)out.push_back(v);return out;}
vector<int> findAnagramIndices(const string&s,const string&p){vector<int>out;if(p.size()>s.size())return out;
    array<int,256>need{},win{};for(unsigned char c:p)++need[c];int m=p.size();
    for(int i=0;i<m;++i)++win[(unsigned char)s[i]];if(win==need)out.push_back(0);
    for(int r=m;r<(int)s.size();++r){--win[(unsigned char)s[r-m]];++win[(unsigned char)s[r]];if(win==need)out.push_back(r-m+1);}return out;}
bool permutationInString(const string&p,const string&s){return !findAnagramIndices(s,p).empty();}

// ============================================================
// TWO POINTERS / WORD MANIPULATION
// ============================================================
string reverseWords(const string&s){stringstream ss(s);string word,out;while(ss>>word){if(!out.empty())out+=' ';out+=word;}
    reverse(out.begin(),out.end()); // reverse whole string then reverse each word
    int start=0;for(int i=0;i<=(int)out.size();++i)if(i==(int)out.size()||out[i]==' ')reverse(out.begin()+start,out.begin()+i),start=i+1;return out;}
string mergeAlternately(const string&a,const string&b){string out;int i=0,j=0;while(i<(int)a.size()||j<(int)b.size()){if(i<(int)a.size())out+=a[i++];if(j<(int)b.size())out+=b[j++];}return out;}

// ============================================================
// SLIDING WINDOW
// ============================================================
int longestSubstringWithoutRepeating(const string&s){array<int,256>last;last.fill(-1);int left=0,best=0;
    for(int r=0;r<(int)s.size();++r){unsigned char c=s[r];left=max(left,last[c]+1);last[c]=r;best=max(best,r-left+1);}return best;}
int longestAtMostKDistinct(const string&s,int k){if(k<0)return 0;array<int,256>f{};int distinct=0,l=0,best=0;
    for(int r=0;r<(int)s.size();++r){if(++f[(unsigned char)s[r]]==1)++distinct;while(distinct>k)if(--f[(unsigned char)s[l++]]==0)--distinct;best=max(best,r-l+1);}return best;}
int longestExactlyKDistinct(const string&s,int k){if(k<=0)return 0;return longestAtMostKDistinct(s,k)-longestAtMostKDistinct(s,k-1);}
int characterReplacement(const string&s,int k){array<int,256>f{};int l=0,maxFreq=0,best=0;
    for(int r=0;r<(int)s.size();++r){maxFreq=max(maxFreq,++f[(unsigned char)s[r]]);while(r-l+1-maxFreq>k)--f[(unsigned char)s[l++]];best=max(best,r-l+1);}return best;}
string minimumWindowSubstring(const string&s,const string&t){if(s.empty()||t.empty())return "";array<int,256>need{};for(unsigned char c:t)++need[c];
    int missing=t.size(),l=0,bestLen=INT_MAX,bestStart=0;
    for(int r=0;r<(int)s.size();++r){unsigned char c=s[r];if(need[c]>0)--missing;--need[c];
        while(missing==0){if(r-l+1<bestLen)bestLen=r-l+1,bestStart=l;unsigned char x=s[l++];if(++need[x]>0)++missing;}}
    return bestLen==INT_MAX?"":s.substr(bestStart,bestLen);}

// ============================================================
// SUBSEQUENCES / LCS
// ============================================================
bool isSubsequence(const string&s,const string&t){int i=0;for(char c:t)if(i<(int)s.size()&&s[i]==c)++i;return i==(int)s.size();}
int longestCommonSubsequence(const string&a,const string&b){int n=a.size(),m=b.size();vector<vector<int>>dp(n+1,vector<int>(m+1));
    for(int i=n-1;i>=0;--i)for(int j=m-1;j>=0;--j)dp[i][j]=a[i]==b[j]?1+dp[i+1][j+1]:max(dp[i+1][j],dp[i][j+1]);return dp[0][0];}
int lcsSpaceOptimized(string a,string b){if(b.size()>a.size())swap(a,b);int m=b.size();vector<int>prev(m+1),cur(m+1);
    for(int i=(int)a.size()-1;i>=0;--i){fill(cur.begin(),cur.end(),0);for(int j=m-1;j>=0;--j)cur[j]=a[i]==b[j]?1+prev[j+1]:max(prev[j],cur[j+1]);prev=cur;}return prev[0];}

// ============================================================
// STRING COMPRESSION / STACK PATTERNS
// ============================================================
string compressString(const string&s){string out;for(int i=0;i<(int)s.size();){int j=i;while(j<(int)s.size()&&s[j]==s[i])++j;out+=s[i];if(j-i>1)out+=to_string(j-i);i=j;}return out;}
string runLengthDecode(const string&s){string out;int i=0;while(i<(int)s.size()){char c=s[i++];int count=0;while(i<(int)s.size()&&isdigit((unsigned char)s[i]))count=count*10+s[i++]-'0';if(!count)count=1;out.append(count,c);}return out;}
bool validParentheses(const string&s){string st;for(char c:s){if(c=='('||c=='['||c=='{')st+=c;else{if(st.empty())return false;char top=st.back();st.pop_back();if((c==')'&&top!='(')||(c==']'&&top!='[')||(c=='}'&&top!='{'))return false;}}return st.empty();}
string removeAdjacentDuplicates(const string&s){string st;for(char c:s)if(!st.empty()&&st.back()==c)st.pop_back();else st+=c;return st;}
string removeAdjacentDuplicatesK(const string&s,int k){vector<pair<char,int>>st;for(char c:s){if(!st.empty()&&st.back().first==c)++st.back().second;else st.push_back({c,1});if(!st.empty()&&st.back().second==k)st.pop_back();}
    string out;for(auto [c,n]:st)out.append(n,c);return out;}
string decodeString(const string&s){vector<pair<string,int>>st;string cur;int num=0;for(char c:s){if(isdigit((unsigned char)c))num=num*10+c-'0';else if(c=='['){st.push_back({cur,num});cur.clear();num=0;}else if(c==']'){auto [prev,k]=st.back();st.pop_back();string tmp;while(k--)tmp+=cur;cur=prev+tmp;}else cur+=c;}return cur;}

// ============================================================
// PARSING / CONVERSION / STRING ARITHMETIC
// ============================================================
int myAtoi(const string&s){int i=0,n=s.size();while(i<n&&isspace((unsigned char)s[i]))++i;int sign=1;if(i<n&&(s[i]=='+'||s[i]=='-')){if(s[i++]=='-')sign=-1;}
    long long val=0;while(i<n&&isdigit((unsigned char)s[i])){val=val*10+s[i++]-'0';if(sign*val>INT_MAX)return INT_MAX;if(sign*val<INT_MIN)return INT_MIN;}return (int)(sign*val);}
string integerToString(long long x){return to_string(x);}
string addBinary(string a,string b){int i=a.size()-1,j=b.size()-1,carry=0;string out;while(i>=0||j>=0||carry){int sum=carry;if(i>=0)sum+=a[i--]-'0';if(j>=0)sum+=b[j--]-'0';out+=char('0'+sum%2);carry=sum/2;}reverse(out.begin(),out.end());return out;}
string addStrings(string a,string b){int i=a.size()-1,j=b.size()-1,carry=0;string out;while(i>=0||j>=0||carry){int sum=carry;if(i>=0)sum+=a[i--]-'0';if(j>=0)sum+=b[j--]-'0';out+=char('0'+sum%10);carry=sum/10;}reverse(out.begin(),out.end());return out;}
string multiplyStrings(const string&a,const string&b){if(a=="0"||b=="0")return "0";int n=a.size(),m=b.size();vector<int>res(n+m);
    for(int i=n-1;i>=0;--i)for(int j=m-1;j>=0;--j){int x=(a[i]-'0')*(b[j]-'0')+res[i+j+1];res[i+j+1]=x%10;res[i+j]+=x/10;}
    string out;for(int x:res)out+=char('0'+x);while(out.size()>1&&out[0]=='0')out.erase(out.begin());return out;}

// ============================================================
// KMP PREFIX FUNCTION / LPS
// ============================================================
vector<int> buildLPS(const string&p){vector<int>lps(p.size());int len=0,i=1;while(i<(int)p.size()){if(p[i]==p[len])lps[i++]=++len;else if(len)len=lps[len-1];else lps[i++]=0;}return lps;}
int kmpSearch(const string&t,const string&p){if(p.empty())return 0;auto lps=buildLPS(p);int i=0,j=0;while(i<(int)t.size()){
    if(t[i]==p[j]){++i;++j;if(j==(int)p.size())return i-j;}else if(j)j=lps[j-1];else ++i;}return -1;}
vector<int> kmpFindAll(const string&t,const string&p){vector<int>out;if(p.empty()){for(int i=0;i<=(int)t.size();++i)out.push_back(i);return out;}auto lps=buildLPS(p);int i=0,j=0;
    while(i<(int)t.size()){if(t[i]==p[j]){++i;++j;if(j==(int)p.size()){out.push_back(i-j);j=lps[j-1];}}else if(j)j=lps[j-1];else ++i;}return out;}

// ============================================================
// Z ALGORITHM / PATTERN SEARCH
// ============================================================
vector<int> zAlgorithm(const string&s){int n=s.size();vector<int>z(n);if(n)z[0]=n;int l=0,r=0;for(int i=1;i<n;++i){if(i<=r)z[i]=min(r-i+1,z[i-l]);while(i+z[i]<n&&s[z[i]]==s[i+z[i]])++z[i];if(i+z[i]-1>r)l=i,r=i+z[i]-1;}return z;}
int zSearch(const string&t,const string&p){if(p.empty())return 0;string x=p+"$"+t;auto z=zAlgorithm(x);for(int i=(int)p.size()+1;i<(int)x.size();++i)if(z[i]>=(int)p.size())return i-(int)p.size()-1;return -1;}
int naivePatternSearch(const string&t,const string&p){if(p.empty())return 0;for(int i=0;i+(int)p.size()<=(int)t.size();++i)if(t.compare(i,p.size(),p)==0)return i;return -1;}

// ============================================================
// RABIN-KARP (ROLLING HASH; verify candidate on hash match)
// ============================================================
int rabinKarpSearch(const string&t,const string&p){if(p.empty())return 0;if(p.size()>t.size())return -1;
    const long long base=256,mod=1000000007;int m=p.size();long long ph=0,wh=0,power=1;
    for(int i=1;i<m;++i)power=power*base%mod;for(int i=0;i<m;++i){ph=(ph*base+(unsigned char)p[i])%mod;wh=(wh*base+(unsigned char)t[i])%mod;}
    for(int s=0;s+m<=(int)t.size();++s){if(ph==wh&&t.compare(s,m,p)==0)return s;if(s+m<(int)t.size()){wh=(wh-(unsigned char)t[s]*power%mod+mod)%mod;wh=(wh*base+(unsigned char)t[s+m])%mod;}}return -1;}

// ============================================================
// TRIE / AUTOCOMPLETE
// ============================================================
struct TrieNode {unordered_map<char,TrieNode*>children;bool end=false;};
struct Trie {TrieNode*root=new TrieNode();
    void insert(const string&w){TrieNode*n=root;for(char c:w){if(!n->children.count(c))n->children[c]=new TrieNode();n=n->children[c];}n->end=true;}
    bool search(const string&w)const{TrieNode*n=root;for(char c:w){if(!n->children.count(c))return false;n=n->children.at(c);}return n->end;}
    bool startsWith(const string&p)const{TrieNode*n=root;for(char c:p){if(!n->children.count(c))return false;n=n->children.at(c);}return true;}
    vector<string> suggestions(const string&prefix){TrieNode*n=root;for(char c:prefix){if(!n->children.count(c))return {};n=n->children[c];}vector<string>out;string path=prefix;
        function<void(TrieNode*)>dfs=[&](TrieNode*x){if(x->end)out.push_back(path);for(auto [c,ch]:x->children){path+=c;dfs(ch);path.pop_back();}};dfs(n);return out;}
};

// ============================================================
// WORD PATTERN / ISOMORPHISM / CUSTOM ORDER
// ============================================================
bool wordPattern(const string&pattern,const string&s){stringstream ss(s);vector<string>w;string x;while(ss>>x)w.push_back(x);if(pattern.size()!=w.size())return false;
    unordered_map<char,string>a;unordered_map<string,char>b;for(int i=0;i<(int)pattern.size();++i){char c=pattern[i];if(a.count(c)&&a[c]!=w[i])return false;if(b.count(w[i])&&b[w[i]]!=c)return false;a[c]=w[i];b[w[i]]=c;}return true;}
bool isomorphicStrings(const string&s,const string&t){if(s.size()!=t.size())return false;array<int,256>a,b;a.fill(-1);b.fill(-1);for(int i=0;i<(int)s.size();++i){unsigned char x=s[i],y=t[i];if(a[x]!=-1&&a[x]!=y)return false;if(b[y]!=-1&&b[y]!=x)return false;a[x]=y;b[y]=x;}return true;}
string customSortString(const string&order,string s){array<int,256>rank;rank.fill((int)order.size());for(int i=0;i<(int)order.size();++i)rank[(unsigned char)order[i]]=i;stable_sort(s.begin(),s.end(),[&](char a,char b){return rank[(unsigned char)a]<rank[(unsigned char)b];});return s;}

// ============================================================
// GREEDY PATTERNS: UNIQUE SMALL LEXICOGRAPHICAL STRING / PARTITION
// ============================================================
string removeDuplicateLetters(const string&s){array<int,256>last{};for(int i=0;i<(int)s.size();++i)last[(unsigned char)s[i]]=i;array<int,256>in{};string st;
    for(int i=0;i<(int)s.size();++i){unsigned char c=s[i];if(in[c])continue;while(!st.empty()&&(unsigned char)st.back()>c&&last[(unsigned char)st.back()]>i){in[(unsigned char)st.back()]=0;st.pop_back();}st+=c;in[c]=1;}return st;}
vector<int> partitionLabels(const string&s){array<int,256>last{};for(int i=0;i<(int)s.size();++i)last[(unsigned char)s[i]]=i;vector<int>out;int start=0,end=0;
    for(int i=0;i<(int)s.size();++i){end=max(end,last[(unsigned char)s[i]]);if(i==end){out.push_back(end-start+1);start=i+1;}}return out;}
string longestCommonPrefix(const vector<string>&v){if(v.empty())return "";string p=v[0];for(int i=1;i<(int)v.size();++i){while(v[i].compare(0,p.size(),p)!=0){if(p.empty())return "";p.pop_back();}}return p;}
int longestBorder(const string&s){if(s.empty())return 0;return buildLPS(s).back();}

// ============================================================
// STRING DYNAMIC PROGRAMMING
// ============================================================
int editDistance(const string&a,const string&b){int m=b.size();vector<int>prev(m+1),cur(m+1);iota(prev.begin(),prev.end(),0);
    for(int i=1;i<=(int)a.size();++i){cur[0]=i;for(int j=1;j<=m;++j)cur[j]=a[i-1]==b[j-1]?prev[j-1]:1+min({prev[j],cur[j-1],prev[j-1]});prev=cur;}return prev[m];}
long long distinctSubsequences(const string&s,const string&t){vector<long long>dp(t.size()+1);dp[0]=1;for(char c:s)for(int j=(int)t.size()-1;j>=0;--j)if(c==t[j])dp[j+1]+=dp[j];return dp.back();}

// ============================================================
// COMPLEXITY CHEAT SHEET
// Basic scans/frequency: O(n); two pointers/sliding window: O(n)
// Expand-around-center palindrome: O(n^2); LCS/edit distance: O(n*m)
// KMP/Z: O(n+m); Rabin-Karp: average O(n+m), worst O(n*m) with collisions
// Trie insert/search: O(length); memory depends on total stored characters.
// ============================================================

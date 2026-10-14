# include <iostream>
# include <vector>
# include <queue>
# include <deque>
# include <stack>
# include <set>
# include <string>
# include <algorithm>
# include <cstdio>
# include <cstdlib>
# include <map>
# include <cmath>
# include <bitset>
# include <list>
# include <sstream>

using namespace std;

bool cmp(const pair<char,int>& a, const pair<char, int>& b)
{
    return (a.second < b.second);
}

int main(){
 //   freopen("input.txt", "r", stdin);
   //  freopen("output.txt", "w", stdout);
    
    map<char, int> see;
    string base;
    cin >> base;
    int k ; cin >> k;
    for(int i=0; i<base.size(); ++i)
    {
        ++see[base[i]];
    }
    
    vector<pair<char, int> > que;
    for(auto it = see.begin(); it != see.end(); ++it)
    {
        que.push_back( make_pair(it->first, it->second) );
    }       
    sort(que.begin(), que.end(), cmp);
    int num = que.size();
    map<char, bool> erase;
    for(int i=0; num > 0 && k>0 && i<que.size(); ++i)
    {
        if (k - que[i].second < 0) break;
        k -= que[i].second;
        erase[que[i].first] = true;
        --num;
    }
    
    cout << num << endl;
    
    for(int i=0; i<base.size(); ++i)
    {
        char& ch = base[i];
        if (erase[ch] && see[ch]) --see[ch];
        else putchar(ch);
    }
    
    return 0;
}
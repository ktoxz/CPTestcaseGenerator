#include<bits/stdc++.h>
using namespace std;
 
#define ll long long int
#define vi vector<ll> 
#define matrix vector< vector<ll> >
#define pb push_back
#define mp make_pair
#define rep(i,a,b) for(ll i = a;i<b;i++)
#define rev_rep(i,b,a) for(ll i=b;i>=a;i--)
 
const ll mod = 1e9 + 7;
//ll arr1[8]={0,0,1,1,1,-1,-1,-1};
//ll arr2[8]={1,-1,0,1,-1,0,1,-1};

bool cmp(pair<int,int> a, pair<int,int> b){
    return a.first > b.first;
}

int main(){
    ll n;
    cin>>n;
    string s1;
    string s2;
    cin>>s1>>s2;
    ll cnt = 0;
    //vector<bool> state(n);
    vector<pair<char,char>> vec1;
    vector<pair<char,char>> vec2;
    
    rep(i,0,n/2){
        vec1.pb(mp(s1[i],s1[n-i-1]));
        vec2.pb(mp(s2[i],s2[n-i-1]));
    }
    rep(i,0,vec1.size()){
       // cout<<vec1[i].first<<" "<<vec1[i].second<<endl;
        //cout<<vec2[i].first<<" "<<vec2[i].second<<endl;
        if(vec1[i].first == vec2[i].first && vec1[i].second == vec2[i].second){
          //  cout<<1<<endl;
            continue;
        }   
        else if(vec1[i].first == vec1[i].second && vec2[i].first == vec2[i].second){
            //cout<<11<<endl;
            continue;
        }
        else if(vec1[i].first == vec2[i].second && vec2[i].first == vec1[i].second){
            //cout<<12<<endl;
            continue;
        }
        else if(vec1[i].first == vec1[i].second && vec2[i].first != vec2[i].second){
            if(vec1[i].first != vec2[i].first && vec1[i].second != vec2[i].second){
                cnt += 2;
            }
            else{
                cnt += 1;
            }
        }
        else{
            set<char> setds;
            setds.insert(vec1[i].first);
            setds.insert(vec1[i].second);
            setds.insert(vec2[i].first);
            setds.insert(vec2[i].second);
            
            if(setds.size()==2 || setds.size() == 3){
                cnt += 1;
            }
            else if(setds.size() == 4){
                cnt += 2;
            }
        }
        //cout<<cnt<<endl;
    }
    //cout<<cnt<<endl;
    if(n & 1){
        if(s1[n/2] != s2[n/2]){
            cnt++;
        }
    }
    cout<<cnt;
}
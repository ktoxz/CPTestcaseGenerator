#include<bits/stdc++.h>

#define fi first

#define se second

#define mp make_pair

#define pb push_back

#define popb pop_back()

#define sz size()

#define mod 1000000007

using namespace std;

typedef long long ll;

///////////////////////////////////////////

string s,t;

map<char,ll>mapp;

map<char,ll>mapp1;

set<char>sett;

ll k,n=25;

char c;

ll ma=0,r;

vector< pair<ll,char> > v;

int main(){

  ios_base::sync_with_stdio(0);

	    cin.tie(NULL);

  cin>>s;

  cin>>k;

  for(ll i=0;i<s.sz;i++){

       mapp[s[i]]++;

  }

  for(ll i='a';i<='z';i++){

     v.pb(mp(mapp[i],i));

  }

  sort(v.begin(),v.end());

  //reverse(v.begin(),v.end());

  /*for(ll i=0;i<v.sz;i++){

    cout<<v[i].fi<<" "<<v[i].se<<endl;

  }*/

  for(ll i=0;i<v.sz;i++){

     if(v[i].fi<=k){

        k-=v[i].fi;

        mapp1[v[i].se]=1;

     }

     else{

        c=v[i].se;

        r=k;

        /*for(ll j=0;j<s.sz;j++){

            if(!mapp1[s[j]]){

                t+=s[j];

            }

        }*/

        break;

     }

  }

  for(ll i=0;i<s.sz;i++){

      if(s[i]==c && r>0){

         r--;

         continue;

      }

      if(!mapp1[s[i]]){

        sett.insert(s[i]);

      t+=s[i];

      }

  }

  cout<<sett.sz<<endl;

  cout<<t<<endl;

}
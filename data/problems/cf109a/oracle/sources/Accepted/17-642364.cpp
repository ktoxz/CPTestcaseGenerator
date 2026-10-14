#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <deque>
#include <set>
#include <map>
#include <utility>
#include <string>
#include <cstring>
#include <queue>
#include <algorithm>
#include <cmath>
using namespace std;
#define fi first
#define se second
#define pb(a) push_back(a)
#define sz(a) ((int)(a).size())
#define mp make_pair
#define EPS 1E-9
typedef long long ll;
typedef long double ld;
typedef pair<int,int> pii;
int main(){
  int S;
  cin>>S;
  int br4=1000000000,br7=1000000000;
  for(int i=0;i<S;++i){
   if(S-4*i<0 || (S-4*i)%7!=0)continue;
   int b4=i,b7=(S-4*i)/7;
   if(br4+br7>b4+b7 || (br4+br7==b4+b7 && br4<b4)){br4=b4; br7=b7;}
                      }
  if(br4==1000000000)cout<<-1<<'\n';
  else{
   for(int i=0;i<br4;++i)cout<<4;
   for(int i=0;i<br7;++i)cout<<7;
   cout<<'\n';
      }
  //system("pause");
  return 0;
}
/*
                                                                           __                _________
                                                                          /  \              /  ______/
                                                                         /    \            /  /
                                                                        /  __  \          /  /
                                                                       /  /  \  \         |  |
                                                                      /  /____\  \        \  \
                                                                     /  ________  \        \  \______
                                                                    /__/        \__\        \________\
	
	I_love_Hacked;
	I_hate_pretest past;
	I_love_STP
	
    coder:xxjAc
    date:2018/7/16
		    
    I_love_Ac;
    I_hate_WA;
    I_hate_Tle;
    I_hate_RE;
    I_hate_CE;
    I_hate_Mle;
    
    I love Accepts very much;
    
    I_don't_love_I_love_zzq
	I_hate_zzq
       
    cd Desktop
    g++ xxjAc.cpp -o std
    ./std
    
    #prag\
    ma GCC optimize("Ofast")
    (O2,O3,Ofast)
*/
#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>
#include <ctime>
#define ll long long 
using namespace std;
const int inf=2e9+7;
const ll linf=1e18+7;
string a,b;
int n;
char c1,c2,c3,c4;
int go(){
	if (c1==c2 && c3==c4){
		return 0;
	}
	if (c1==c3 && c2==c4){
		return 0;
	}
	if (c1==c4 && c3==c2){
		return 0;
	}
	if (c1!=c2 && c3==c4){
		return 1;
	}
	if (c1!=c3 && c2==c4){
		return 1;
	}
	if (c1!=c4 && c2==c3){
		return 1;
	}
	if (c2!=c3 && c1==c4){
		return 1;
	}
	if (c2!=c4 && c1==c3){
		return 1;
	}
	if (c3!=c4 && c1==c2){
		return 2;
	}
	return 2;
}
int main(){
	cin>>n;
	cin>>a;
	cin>>b;
	int ans=0;
	if (n%2==1){
		c1=a[n/2];
		c2=b[n/2];
		if (c1!=c2){
			ans++;
		}
	}
	//cout<<ans<<endl;
	for (int i=0;i<n/2;i++){
		c1=a[i];
	    c2=a[n-i-1];
	    c3=b[i];
		c4=b[n-i-1];
    	//cout<<c1<<' '<<c2<<' '<<c3<<' '<<c4<<endl;
		ans+=go();
	}
	cout<<ans<<endl;
	return 0;
}
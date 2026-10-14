#include<iostream>
#include<vector>
#include<map>
#include<algorithm>
#include<cstdio>
#include<cmath>
#include<cstdlib>
#include<cstring>
#include<queue>
#include<fstream>
#include<sstream>
#include<stack>
#include<list>
#include<deque>
#include<bitset>
#include<utility>
#include<climits>
#include<iomanip>
#include<ctime>
using namespace std;
#define SORT(c) sort((c).begin(),(c).end());
#define INF INT_MAX/3
#define pb push_back
#define MP make_pair
#define pii pair<int,int>
#define pcc pair<char,char>
#define pic pair<int,char>
#define pci pair<char,int>
#define VS vector<string>
#define VI vector<int>
#define pi 3.141592653589793
#define in scanf
#define out printf
#define ll long long
#define ull unsigned long long
template<typename T>inline T  S(T a){
	return a*a;
}
template<class T>inline string tostring(T a){
	ostringstream os("");
	os << a;
	return os.str();
}
template<typename T>inline ll tolong(T a){
	ll res;
	istringstream os(a);
	os>>res;
	return res;
}
template<typename T>inline T gcd(T a, T b){
	if (b == 0)return a;
	else return gcd(b, a % b);
}
template<typename T>inline T bigmod(T a, T b, T m)
{
	if (b == 0)return 1;
	else if (b % 2 == 0)return S(bigmod(a, b / 2, m)) % m;
	else return (a % m*bigmod(a, b - 1, m)) % m;
}
bool comp(pii a,pii b)
{
	if (a.first==b.first)return a.second>b.second;
	else return a.first<b.first;
}
int main()
{
string s;
int a;
freopen("input.txt","r",stdin);
freopen("output.txt","w",stdout);
cin>>s>>a;
if(s=="front")
{
if(a==1)cout<<"L"<<endl;
else cout<<"R"<<endl;
}
else
{
if(a!=1)cout<<"L"<<endl;
else cout<<"R"<<endl;
}

return 0;
}
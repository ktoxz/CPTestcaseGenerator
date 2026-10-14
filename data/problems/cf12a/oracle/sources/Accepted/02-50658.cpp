/*
Author : OmarEl-Mohandes
PROG   : A
LANG   : C++
*/
#include <map>
#include <deque>
#include <queue>
#include <stack>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <vector>
#include <set>
#include <complex>
#include <memory.h>
using namespace std;
#define pb push_back
#define all(v) v.begin(),v.end()
#define sz size()
#define rep(i,m) for(int i=0;i<m;i++)
#define REP(i,k,m) for(int i=k;i<m;i++)
#define mem(a,b) memset(a,b,sizeof(a))
#define mp make_pair
typedef stringstream ss;
typedef pair<int, int> pii;
typedef vector<pii> vpii;
typedef vector<string> vs;
typedef vector<int> vi;
typedef vector<vector<int> > vii;
typedef long long ll;
#define oo ((int)1e9)

int main()
{
	//freopen("A.in" , "rt" , stdin);
	//freopen("A.out" , "wt" , stdout);
	string s1=""  , s2="" , s3="";
	string t1="" , t2="" , t3="";
	getline(cin , s1);
	getline(cin , s2);
	getline(cin , s3);
	if(s1.size() && s2.size() && s3.size())
	t1 = s1[0] + s2[0] + s3[0];
	if(s1.size()==2 && s2.size()==2 && s3.size()==2)
	t2 = s1[1] + s2[1] + s3[1];
	if(s1.size()==3 && s2.size()==3 && s3.size()==3)
	t3 = s1[2] + s2[2] + s3[2];
	reverse(all(s1));
	reverse(all(t1));
	if(s1 == s3 && t1 == t3)cout << "YES" << endl;
	else cout <<"NO" << endl;;
	return 0;
}
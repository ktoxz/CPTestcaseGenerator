#include<iostream>
#include<cstdlib>
#include<cstdio>
#include<cmath>
#include<cstring>
#include<algorithm>
using namespace std;

string door,ans;
int a;

int main()
{
	freopen("input.txt","r",stdin);
	freopen("output.txt","w",stdout);
	cin >> door;
	cin >> a;
	if (door=="front")
	{
		if (a==1) ans="L";else ans="R";
	}
	else
	{
		if (a==1) ans="R";else ans="L";
	}
	cout << ans << endl;

	return 0;
}
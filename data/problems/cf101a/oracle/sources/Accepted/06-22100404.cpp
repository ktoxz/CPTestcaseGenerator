#include<bits/stdc++.h>
using namespace std;
int c[255],k;
string s;
int main()
{
	cin>>s>>k;
	for (int i=0;i<s.size();i++) c[s[i]]++;
	for (int i=0;i<k;i++)
	{
		int ind=-1;
		for (int j=0;j<255;j++) 
			if (c[j] && (ind==-1 || c[ind]>c[j])) 
				ind=j;
		if (ind==-1) break;
		c[ind]--;
	}
	int m=0;
	for (int i=0;i<255;i++) if (c[i]) m++;
	cout<<m<<endl;
	for (int i=0;i<s.size();i++) if (c[s[i]]) cout<<s[i],c[s[i]]--;
	return 0;
}
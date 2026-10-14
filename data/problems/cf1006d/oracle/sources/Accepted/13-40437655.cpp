#include<bits/stdc++.h>
using namespace std;
const int N=100005;
char s[4];
string s1,s2;
int main()
{
	int n,sum=0;
	cin>>n>>s1>>s2;
	for(int i=0;i<n/2;i++)
	{
		s[0]=s1[i];
		s[1]=s1[n-i-1];
		s[2]=s2[i];
		s[3]=s2[n-i-1];
		if((s[0]==s[2]&&s[1]==s[3])||(s[0]==s[3]&&s[1]==s[2])||(s[0]==s[1]&&s[2]==s[3]))
			continue;
		else if(s[0]==s[2]||s[1]==s[3]||s[0]==s[3]||s[1]==s[2]||s[2]==s[3])
			sum+=1;
		else
			sum+=2;
	}
	if(n%2&&s1[n/2]!=s2[n/2])
		sum+=1;
	cout<<sum<<endl;
	return 0;
}
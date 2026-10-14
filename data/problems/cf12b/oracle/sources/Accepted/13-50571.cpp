#include <string>
#include <iostream>
#include <algorithm>
#include <cstdlib>
using namespace std;

int main()
{
	string s,t;
	
	cin>>s;
	cin>>t;
	sort(s.begin(),s.end());
	if (s[s.size()-1]=='0' && s==t) {
		cout<<"OK"<<endl;
		exit(0);
	}

	int i;
	for (i=0;i<s.size();++i) if (s[i]!='0') break;

	swap(s[i],s[0]);
	if (s==t)
		cout<<"OK"<<endl;
	else
		cout<<"WRONG_ANSWER"<<endl;

	return 0;
}
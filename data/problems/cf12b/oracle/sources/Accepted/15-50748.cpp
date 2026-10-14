#include <iostream>
#include <cstdio>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <deque>
using namespace std;
vector<char> a;
deque<char> b;
string s1,s2,st; 
int main(){
	cin>>s1>>s2;
	for (int i=0;i<s1.length();i++){
		a.push_back(s1[i]);
	}
	sort(a.begin(),a.end());
	bool is=false;
	for (int i=0;i<a.size();i++){
		if (a[i]!='0' && !is){
			is=true;
			b.push_front(a[i]);
		}
		else	b.push_back(a[i]);
	}
	st="";
	for (int i=0;i<b.size();i++){
		st+=b[i];
	}
	if (st==s2){
		cout<<"OK"<<endl;
	}
	else{
		cout<<"WRONG_ANSWER"<<endl;
	}
	return 0;
}
#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;

int main(){
	
	string a,b,x="";
	vector <char> vec;
	char temp;
	cin >> a >> b;
	
	if(a[0]==0) {
		cout << "WRONG_ANSWER"<<endl;
		return 0;
	}
	
	for(int i=0;i<a.length();i++){
		vec.push_back(a[i]);
	}
	
	sort(vec.begin(),vec.end());
	
	if(vec[0]=='0'){
		for(int i=0;i<vec.size();i++){
			if(vec[i]!='0'){
				temp = vec[i];
				vec[i]=vec[0];
				vec[0]=temp;
				break;
			}
			
		}
	}
	
	for(int i=0;i<vec.size();i++){
		x +=vec[i];
	}
	
	if(x==b) cout <<"OK"<<endl;
	else cout << "WRONG_ANSWER"<<endl;
	
return 0;
}
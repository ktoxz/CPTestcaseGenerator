#include<iostream>

using namespace std;

char a[20];

int main(){

	

	for(int i=1;i<=9;i++) 	cin>>a[i];

	

	

	for(int i=1;i<=4;i++){

		if(a[i]!=a[10-i]){

			cout<<"NO";

			return 0;

		}

	}

	

	cout<<"YES";

	

	

	

	

}
#include<bits/stdc++.h>

using namespace std;



const int max_n=100+10;

int s[max_n],r[max_n],h[max_n],p[max_n];

bool lap[max_n];



int main(){

	int n;

	cin>>n;

	for(int i=0;i<n;i++)

		cin>>s[i]>>r[i]>>h[i]>>p[i];

	for(int i=0;i<n;i++){

		for(int j=0;j<n;j++){

			if(s[i]<s[j] && r[i]<r[j] && h[i]<h[j] && p[i]<p[j])

				lap[i]=true;

		}

	}

	int mini;

	for(mini=0;lap[mini];mini++){}

	for(int i=mini;i<n;i++){

		if(!lap[i]){

			if(p[mini]>p[i])

				mini=i;

		}

	}

	cout<<mini+1;

}
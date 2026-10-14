#include<bits/stdc++.h>

using namespace std;

int main()

{

	int a,b,n;

	cin>>a>>b>>n;

	while(1){

		n=n-__gcd(a,n);

		if(n<=0){

			printf("0\n");

			break;

		}

		n=n-__gcd(b,n);

		if(n<=0){

			printf("1\n");

			break;

		}

	}

}
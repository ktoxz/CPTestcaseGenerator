#include<iostream>

#include<cmath>

using namespace std;

int main()

{

	long long int n,k;

	cin>>k>>n;

	long long int q=n;

	long long int o=0;

	while((n/k)>1)

	{

		n=n/k;

		o++;

	//	cout<<n<<endl;

	}

//	cout<<n<<endl;

        long long int i=int(pow(k,o+1));

        cerr<<q;

	if(i==q)

	{

	        cout<<"YES"<<endl;

	        cout<<o;

	}

	else

	{

		cout<<"NO";

	}

}
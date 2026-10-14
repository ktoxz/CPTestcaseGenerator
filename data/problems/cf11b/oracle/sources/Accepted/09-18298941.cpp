#include<iostream>

#include<cstdio>

using namespace std;

int main()

{

	long long n,i;

	cin>>n;

	if(n<=-1)

	{

		n=n*(-1);

	}

	if(n==0)

	{

		cout<<0<<"\n";

	}

	else

	{

		long long d;

		for(i=1; ;i++)

		{

			d=i*(i+1);

			d=d/2;

			if(d==n)

			{ 

				break;

			}

			else if((d-n)%2==0 && d>n)

			{

				 break;

			}

		}

		cout<<i<<"\n";

	}

}
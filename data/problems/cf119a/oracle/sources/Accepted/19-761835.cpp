#include <iostream>

using namespace std;

int nod (int a, int b)
{
        if (b == 0)
                return a;
        else
                return nod (b, a % b);
}

int main()
{
	int a,b,n;
	cin >> a;
	cin>> b;
	cin>> n;
	bool flag = 0;
	while(n > 0)
	{
		if(flag == 0)
		{
			n -= nod( a, n );
			flag = 1;
			if(n == 0) cout << "0";
		}
		else
		{
			n -= nod( b, n );
			flag = 0;
			if(n == 0) cout << "1";
		}

	}
	return 0;
}
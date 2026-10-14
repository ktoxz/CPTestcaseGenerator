#include <iostream>

#include <cmath>

using namespace std;



int main()

{

	long long int x,a,b,c;

	cin >> a;

	a = abs(a);

	b = 0;

	c = 0;

	while (b < a || (b-a) %  2 != 0)

	{

		c++;

		b = b + c;

	}

	cout << c <<  "\n";

}
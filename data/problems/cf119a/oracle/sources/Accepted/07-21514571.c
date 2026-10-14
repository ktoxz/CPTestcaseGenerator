#include<stdio.h>



int gcd (int a, int b) {

	

	int c;

	

	if (b == 0)

	

		return a;

		

	else {

		

		c = gcd(b, a % b);

	}

}



int main()



{

	int m, n, a, b;

	

	scanf("%d %d %d", &a, &b, &n);

	

	while (1) {

		

		n -= gcd(a, n);

		

		if (n <= 0) {

		

			printf("0\n");

			

			break;

		}

		

		n -= gcd(b, n);

		

		if (n <= 0) {

		

			printf("1\n");

			

			break;

		}

	}

	

	return 0;

}
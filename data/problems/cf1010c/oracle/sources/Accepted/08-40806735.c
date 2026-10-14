#include <stdio.h>

int gcd (int a, int b) 
{
	int r;
	while (b > 0) 
	{
		r = a % b;
		a = b;
		b = r;
	}

	return a;
}

int main() {
	int i;

	int n, k, a, tmp, nsol;

	scanf("%d %d", &n, &k);
	scanf("%d", &a);
	for (i = 1; i < n; i++) {
		scanf("%d", &tmp);
		a = gcd(a, tmp);
	}
	a = gcd(a, k);

	nsol = k/a;
	tmp = 0;
	printf("%d\n", nsol);
	for (i = 0; i < nsol; i++) {
		printf("%d ", tmp);
		tmp += a;
	}
	printf("\n");
}
#include<stdio.h>

int main()
{
	int t, k, i, j, n;
	
	scanf("%d", &n);
	if(n<11||n>21)
		printf("0");
	else if((n>10&&n<20)||(n==21))
	printf("4");
	else
		printf("15");
	return 0;
}
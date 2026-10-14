#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#include <string.h>
#define max 200000
int main()
{
	char s[max];
	scanf("%s",s);
	int l = strlen(s);
	int ptr = -1;
	long long sum = 0,ctr = 0;
	for (int i = 0; i<l; i++)
	{
		sum = 0;
		for (int j = i; j>ptr; j--)
		{
			sum += s[j]-'0';
			if (sum%3 == 0)
			{
				ctr++;
				ptr = i;
			}
		}
	}
	printf("%lld", ctr);
	return 0;
}
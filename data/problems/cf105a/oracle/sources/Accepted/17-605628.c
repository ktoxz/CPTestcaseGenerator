#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MAXN 55

struct node
{
	char s[MAXN];
	int a;
};

void sort (struct node a[MAXN], int l, int r)
{
	int i, j;
	struct node x, y;
	i = l; j = r; x = a[(l+r)/2];
	while (i <= j)
	{
		while (strcmp(a[i].s, x.s) < 0) i++;
		while (strcmp(a[j].s, x.s) > 0) j--;
		if (i <= j)
		{
			y = a[i]; a[i] = a[j]; a[j] = y;
			i++; j--;
		}
	}
	if (l < j) sort(a,l,j);
	if (i < r) sort(a,i,r);
}

int main ()
{
	int N, M, K;
	scanf("%d %d 0.%d\n",&N,&M,&K);
	static struct node a[MAXN];
	int i;
	int ac = 0;
	for (i = 0; i < N; i++)
	{
		scanf("%s %d\n",a[ac].s,&(a[ac].a));
		a[ac].a = (a[ac].a * K) / 100;
		if (a[ac].a >= 100) ac++;
	}
	int orig = ac;
	int j;
	for (i = 0; i < M; i++)
	{
		scanf("%s\n",a[ac].s);
		a[ac].a = 0;
		j = 0;
		while (j < orig)
		{
			if (strcmp(a[ac].s, a[j].s) == 0) break;
			j++;
		}
		if (j == orig) ac++;
	}
	sort(a,0,ac-1);
	printf("%d\n",ac);
	for (i = 0; i < ac; i++)
	{
		printf("%s %d\n",a[i].s,a[i].a);
	}
	return 0;
}
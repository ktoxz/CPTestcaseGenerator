#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define INFINITY 1000000000

int main ()
{
	int N, X, Y;
	scanf("%d",&N);
	int resX = INFINITY;
	int resY = INFINITY;
	for (X = 0; (4*X) <= N; X++)
	{
		if (!((N-4*X) % 7))
		{
			Y = (N-4*X) / 7;
			if (((X+Y) < (resX+resY)) || (((X+Y) < (resX+resY)) && (X < resX)))
			{
				resX = X;
				resY = Y;
			}
		}
	}
	if (resX == INFINITY) printf("-1\n");
	else
	{
		for (X = 0; X < resX; X++) printf("4");
		for (Y = 0; Y < resY; Y++) printf("7");
		printf("\n");
	}
	return 0;
}
#include <stdio.h>
#include <string.h>
#define MAXN 100

char graph[MAXN][MAXN];
int N;

char flag[MAXN];
char deepth[MAXN];

int N;
int M;

int search_for_loop( int p, int father, int deep)
{
	/*
	printf("visiting %d from %d\n", p, father);
	*/
	flag[p] = 1;
	deepth[p] = deep;
	++deep;
	int i;
	int ret = 0;
	for ( i = 0; i < N; i++)
	{
		if ( graph[p][i])
		{
			int tmp = flag[i] ? ( flag[i] == 1  && i != father ? deepth[p] - deepth[i] : 0) : search_for_loop( i, p, deep);
			/*
			printf("find %d from %d, deepth %d flag %d cur deep %d tmp %d\n", i, p, deepth[i], (int)flag[i], deepth[p], tmp);
			*/
			ret = ret < tmp ? tmp : ret;
		}
	}
	flag[p] = 2;
	/*
	printf("%d %d\n", p, ret);
	*/

	return ret;
}

int main()
{
	while ( scanf("%d %d", &N, &M) == 2)
	{
		memset( graph, 0, sizeof( graph));
		int i;
		for ( i = 0; i < M; i++)
		{
			int s, t;
			scanf("%d %d", &s, &t);
			--s, --t;
			graph[s][t] = 1;
			graph[t][s] = 1;
		}

		char ans = N == M;
		if ( ans)
		{
			memset( flag, 0, sizeof( flag));
			ans &= search_for_loop( 0, -1, 0) > 1;
			for ( i = 0; i < N && ans; i++)
			{
				ans &= flag[i] == 2;
			}

			/*
			memset( flag, 0, sizeof( flag));
			for ( i = 0; i < N && ans; i++)
			{
				if ( isroot[i])
				{
					ans &= !flag[i];

				}
			}
			*/
		}
		printf("%s\n", ans ? "FHTAGN!" : "NO");
	}

	return 0;
}
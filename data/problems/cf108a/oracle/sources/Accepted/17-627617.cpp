#include <cstdio>

int main()
{
	int a, b, i, j;
	bool ok, f;

	while( scanf("%d:%d", &a, &b) != EOF )
	{
		ok = 1;
		f = 1;

		for( i = a; ok && i <= 23; ++i )
		{
			if( f )
			{
				j = b+1;
				f = 0;
			}
			else
				j = 0;
			for( ; ok && j <= 59; ++j )
			{
				if( i/10 == j%10 && i%10 == j/10 )
				{
					ok = 0;
					break;
				}
			}

			if( !ok )
				break;

			if( i == 23 )
				i = -1;
		}

		printf("%.2d:%.2d\n", i, j);
	}

	return 0;
}
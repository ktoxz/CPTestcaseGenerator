#include<iostream>

#include <cstdio>



using namespace std;



int n, current=0;

bool graph[101][101], visited[101] ;



void dfs(int j)

{

	visited[j] = true;

	current++;



	for(int i=1; i<=n; i++)

	{

		if((graph[j][i] || graph[i][j]) && !visited[i])

        {

            dfs(i);

		}

	}

}



int main()

{

    int m, x, y;

	scanf("%d %d",&n, &m);



	for(int i=0; i<m; i++)

	{

		scanf("%d %d", &x, &y);

		graph[x][y] = graph[y][x] = true;

	}



	dfs(1);



	if(current!=n || n!=m)

	{

        printf("NO\n");

	}

	else

	{

        printf("FHTAGN!\n");

	}

}
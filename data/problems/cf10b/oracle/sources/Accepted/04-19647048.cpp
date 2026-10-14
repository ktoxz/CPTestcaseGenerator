#include<bits/stdc++.h>

using namespace std;

const int INF = 0x3f3f3f3f;

int n ,k;

bool vis[105][105];

int cost[105][105];

int main()

{

    scanf("%d%d" , &n , &k);

    int c = (k >> 1) + 1;

    //cout<<c<<endl;

    memset(vis , 0 , sizeof(vis));

    for(int i = 1 ; i <= k ; ++i)

    {

        for(int j = 1 ; j <= k ; ++j)

        {

            cost[i][j] = abs(c - i) + abs(c - j);

            //cout<<cost[i][j]<<" ";

        }

        //cout<<endl;

    }

    for(int x = 1 ; x <= n ; ++x)

    {

        int m;

        scanf("%d" , &m);

        bool flag = 0;

        long long sum = INF;

        int stay = 0, l , r;

        for(int i = 1 ; i <= k ; ++i)

        {

            for(int j = 1 ; j <= k - m + 1 ; ++j)

            {

                long long tmp_sum = 0;

                flag = 0;

                for(int t = 0 ; t < m ; ++t)

                {

                    if(vis[i][j + t])

                    {

                        flag = 1;

                        break;

                    }

                    tmp_sum += cost[i][t + j];

                }

                if(!flag && tmp_sum < sum)

                {

                    stay = i;

                    l = j;

                    r = j + m - 1;

                    sum = tmp_sum;

                }

            }

        }

        if(stay)

        {

            for(int i = 0 ; i < m ; ++i)

                vis[stay][l + i] = 1;

            printf("%d %d %d\n" , stay , l , r);

        }

        else

        {

            printf("-1\n");

        }

    }

    return 0;

}
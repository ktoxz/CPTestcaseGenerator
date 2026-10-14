#include<iostream>
#include<cstdio>
#include<cstring>
#include<queue>
using namespace std;

int main()
{
    int l,now,k,answer,mid;
    char number[200005];
    scanf("%s",&number);
    l = strlen(number);
    now = answer = 0;
    queue <int> mod[2];
    for (int i = 0; i < l; i++)
    {
        k = number[i] - '0';
        if (k % 3 == 0)
        {
            while (!mod[now].empty())
            {
                mod[now].pop();
            }
            answer++;
        }
        else
        {
            mod[now ^ 1].push(k % 3);
            while (!mod[now].empty())
            {
                mid = mod[now].front() + k;
                mod[now].pop();
                mid %= 3;
                if (mid == 0)
                {
                    answer++;
                    while (!mod[now].empty())
                    {
                        mod[now].pop();
                    }
                    while (!mod[now ^ 1].empty())
                    {
                        mod[now ^ 1].pop();
                    }
                    break;
                }
                mod[now ^ 1].push(mid);
            }
            now ^= 1;
        }
    }
    printf("%d\n",answer);
    return 0;
}
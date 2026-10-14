#include <iostream>
#include <cstdio>
#include <algorithm>
#include <queue>
#include <map>
#include <string>
#include <stack>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <set>
#define LL long long
#define INF 0x3f3f3f3f
using namespace std;
const double pi = 2*acos(0.0);
const int maxn = 120000 + 10;

int a[maxn];
int two[50];
map<int,int> mp;

int main()
{
    int ans = 0;
    two[0] = 1;
    for(int i=1;i<32;i++)
        two[i] = two[i-1]*2;
    int n;
    cin >> n;
    for(int i=0;i<n;i++)
    {
        scanf("%d",&a[i]);
        mp[a[i]]++;
    }
    for(int i=0;i<n;i++)
    {
        int flag = 0;
        mp[a[i]]--;
        //printf("%!@!\n");
        for(int j=1;j<32;j++)
        {
            int temp = two[j] - a[i];
            //printf("%d\n",temp);
            if(temp>0&&mp[temp])
            {
                //printf("yes\n");
                flag = 1;
                break;
            }
        }
       // printf("flag=%d\n",flag);
        if(!flag) ans++;
        mp[a[i]]++;
    }
    printf("%d\n",ans);
    return 0;
}
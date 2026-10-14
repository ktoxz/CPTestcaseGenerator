/* 
 * File:   main.cpp
 * Author: luyi0619
 *
 * Created on August 23, 2011, 9:04 PM
 */
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <algorithm>
#include <string>
#include <cctype>
#include <queue>
#include <map>
#include <set>
#include <vector>
/*
 * 
 */
using namespace std;
bool check(int a,int b)
{
    char cmd[10];
    sprintf(cmd,"%02d:%02d\n",a,b);
    if(cmd[0] == cmd[4] && cmd[1] == cmd[3])
        return true;
    else
        return false;
}
int main()
{

    int a,b;
    while(scanf("%d:%d",&a,&b) == 2)
    {
        while(1)
        {
            b ++;
            if(b == 60)
            {
                a ++;
                if(a  == 24)
                    a = 0;
                b = 0;
                
            }
            if(check(a,b))
                    break;
        }
        printf("%02d:%02d\n",a,b);
    }
    return 0;
}
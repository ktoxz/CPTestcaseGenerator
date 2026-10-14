/* 
 * File:   main.c
 * Author: khurshid
 *
 * Created on August 23, 2011, 8:45 PM
 */

#include <stdio.h>
#include <stdlib.h>

/*
 * 
 */
int main(int argc, char** argv)
{
    int n;
    int p;
    int d[1001][1001] = {0};
    int in[1001] = {0};
    int out[1001] = {0};
    int e[1001] = {0};
    int i;
    int t;
    int tank[1001];
    int tap[1001];
    int diam[1001];

    
    scanf("%d %d", &n, &p);
    for(i = 1; i<=p;i++)
    {
        int a,b;
        scanf("%d %d",&a, &b);
        scanf("%d", &d[a][b]);
        in[b] = 1;
        out[a] = 1;
    }

    t = 0;
    for(i = 1; i<= n; i++)
    {
        //agar i ga kiruvchi truba bulmasa, va i hali hisoblanmagan bulsa
        if (!in[i] && !e[i])
        {

            int stack[1001];
            int stack_d[1001];
            int iTop = 0;
            e[i] = 1;//otmetka

            stack[iTop] = i;
            stack_d[iTop] = 10000001;//maximal son
            iTop++;
            
            while ( iTop > 0 )
            {
                int el = stack[--iTop];
                int el_d = stack_d[iTop];
                int j;

                for(j = 1; j <=n ;j++)
                {
                    //agar j - otmetka qilinmagan bulsa va (el, j) orasida truba bulsa
                    if (!e[j] && d[el][j] > 0)
                    {
                        e[j] = 1; //otmetka j
                        stack[iTop] = j;
                        stack_d[iTop] = (el_d < d[el][j])?el_d : d[el][j];
                        iTop++;

                        //agar j - oxirgi truba bulsa  (i,j) juftlikni tanlaymiz
                        if (!out[j])
                        {
                            tank[t] = i;
                            tap[t] = j;
                            diam[t] = (el_d < d[el][j])?el_d : d[el][j];
                            t++;
                        }
                    }
                }
            }
            
           
        }
    }


    printf("%d\n", t);
    for(i = 0; i<t;i++)
    {
        printf("%d %d %d\n", tank[i], tap[i], diam[i]);
    }
    return (EXIT_SUCCESS);
}
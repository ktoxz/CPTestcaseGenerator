#include<stdio.h>

#include<string.h>

#include<stdlib.h>

int main()

{

        char s[10],hh[5],mm[5],var[5],var2[5];

        char i,j,k,l;

        int h,m,flag=0;



        scanf("%s",&s);



        i=s[0];

        j=s[1];

        k=s[3];

        l=s[4]+1;



        for(;i<=50;i++)

        {

                for(;j<=57;j++)

                {

                    for(;k<=53;k++)

                    {

                        for(;l<=57;l++)

                        {

                                if(i==l && j==k)

                                {

                                    if(i==50 && j>51)

                                    {

                                            //printf("%c%c:%c%c\n",i,j,k,l);

                                            break;

                                    }

                                    else

                                    {

                                        //printf("%c%c:%c%c bn\n ",i,j,k,l);

                                        printf("%c%c:%c%c",i,j,k,l);

                                        return 0;

                                    }

                                }

                        }

                        l=48;

                    }

                    k=48;

                }

                j=48;



        }



        if(flag==0)

        {

            printf("00:00");

        }



        return 0;

}
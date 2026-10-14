#include<bits/stdc++.h>

 using namespace std;

 int main()

 {

    /*freopen("input.txt","r",stdin);

    freopen("output.txt","w",stdout);*/

    /*ios_base::sync_with_stdio(0);

    cin.tie(0);

    cout.tie(0);*/

    int w;

    scanf("%d",&w);

    if(w==0)

    {

       printf("%d",0);

       return 0;

    }

    long long n=abs(w);

    long long ans1=0;

    long long ans2=1;

    while((ans1-n)%2!=0 || ans1-n<0)

    {

       ans1=ans1+ans2;

       ans2++;

    }

    printf("%d",ans2-1);

    return 0;

 }

 //s[i].size()

 //a=tolower(a) делает char переменную a маленькой,

//a=toupper(a), делает char переменную a большой

/*



 /*  %с – одиночный символ

     %d – десятичное целое число со знаком

     %f – число с плавающей точкой (десятичное представление)

     %s – строка символов (для строковых переменных)

     %u – десятичное целое без знака

     %% - печать знака процента

     printf(“Ваш возраст = %d, Ваш вес = %f”, age, weigth);

     */



/* if((j<n-abs(i-n/2)) and j>=abs(i-n/2))

          {

             cout << "D";

          }

          else

          {

             cout << "*";

          }*/
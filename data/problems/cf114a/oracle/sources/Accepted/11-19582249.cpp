/***************************************************************

*    __    _____________      _______  _    ______             *

*     |\  /||    | |     |    | |   |  |    | |   |            *

*     | \/ ||____| |---| |____| |---|  |    | |---| -          *

*     |    ||    |     | |    | |   \  |____| |   \ |          *

*    --    --    --|------    ---   ----------------|          *

*                                                              *

*                Name: Mashrur Rashik                          *

*              Inst: University of Dhaka                       *

*                Country : Bangladesh                          *

***************************************************************/



#include<stdio.h>

#include<bits/stdc++.h>

using namespace std;

#define MAX 300300

#define clr(ar) memset(ar, 0, sizeof(ar))

#define fr(i,n); for(i=0;i<n;i++)

#define sc(a) cin>>a

#define pr(a) cout<<a<<endl

typedef long long i64;

typedef unsigned long long ui64;

#define inf (i64) 9e18

#define eps 1e-9

#define pii pair <i64,i64>



/****************************************************************/



i64 power(i64 a,i64 b)

{

    i64 s=1;

    while(b){

        if(b%2!=0) s=s*a;

        b=b/2;

        if(b) a=a*a;

    }

    return s;

}





int main()

{

    bool flag=false;

    i64 a,b,t,s,i;

    sc(a);sc(b);



    for(i=0;;i++)

    {

        t=power(a,i);

        if(t==b){

            flag=true;

            break;

        }

        if(t>b) break;

    }



    if(flag){

        printf("YES\n");

        i--;

        printf("%I64d\n",i);

    }

    else printf("NO\n");

    return 0;

}
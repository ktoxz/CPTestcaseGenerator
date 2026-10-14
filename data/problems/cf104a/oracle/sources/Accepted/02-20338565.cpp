# include<iostream>

# include<string>

# include<cmath>

# include<algorithm>

# include<vector>

# include<map>

# include<queue>

# include<stack>

# include<set>



# define pb push_back

# define mp make_pair

# define ll long long

# define ull unsigned long long

# define sfd(a) scanf("%d",&a)

# define pfd(a) printf("%d",a)

# define sfc(a) scanf("%c",&a)

# define pfc(a) printf("%c",a)

# define sfll(a) scanf("%I64d",&a)

# define pfll(a) printf("%I64d",a);



using namespace std;



const int MAXN=1e6+1;



int n,p[MAXN],dem,ans,pes;



int main(){



scanf("%d",&n);



if(n-10<=9  && n-10>=1 || n-10==11){

    cout<<4;

    return 0;

}



if(n-10==10){

cout<<15;

return 0;

}



else cout<<0;



return 0;

}
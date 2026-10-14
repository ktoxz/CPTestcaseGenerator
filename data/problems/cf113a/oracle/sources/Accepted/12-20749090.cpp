#include <bits/stdc++.h>

using namespace std;



typedef long long ll;

typedef long long LL;

typedef pair<int,int> ii;

typedef vector<ii> vii;

typedef vector<int> vi;



#ifdef DEBUG

    #define cek(x) cout<<x

#else

    #define cek(x) if(false){}

#endif // DEBUG



#define fi first

#define se second

#define INF 1000000000

#define INFLL 1000000000000000000LL

#define EPS 1e-9

#define PI acos(-1.0)

#define pb push_back

#define TC() while(tc--)

#define FOR(i,n) for(int i=0;i<n;i++)

#define FORN(i,n) for(int i=0;i<=n;i++)

#define REP(i,a,b,c) for(int i=a;i<b;i+=c)

#define REPN(i,a,b,c) for(int i=a;i<=b;i+=c)

#define reset(a,b) memset(a,b,sizeof(a))

#define sc(x) scanf("%d",&x)



int main(void){

    bool valid = true;

    bool mas = false;

    bool fem = false;

    bool have = false;

    int now = 0;

    int ct = 0;

    string str;

    while(cin>>str){

        ct++;

        size_t pos = str.rfind("lios");



        if(pos != string::npos && (int)pos == str.length() - 4){

            mas = true;

            if(now > 0)valid = false;

            continue;

        }

        pos = str.rfind("liala");

        if(pos != string::npos && (int) pos == str.length() - 5){

            fem = true;

            if(now > 0)valid = false;

            continue;

        }



        pos = str.rfind("etr");

        if(pos != string::npos && (int) pos == str.length() - 3){

            mas = true;

            have = true;

            if(now >= 1)valid = false;

            if(now == 0)now = 1;

            continue;

        }



        pos = str.rfind("etra");

        if(pos != string::npos && (int) pos == str.length() - 4){

            fem = true;

            have = true;

            if(now >= 1)valid = false;

            if(now == 0)now = 1;

            continue;

        }



        pos = str.rfind("initis");

        if(pos != string:: npos && (int) pos == str.length() - 6){

            mas = true;

            if(now == 0 && ct > 1)valid = false;

            now = 2;

            continue;

        }



        pos = str.rfind("inites");

        if(pos != string::npos && (int) pos == str.length() - 6){

            fem = true;

            if(now == 0 && ct > 1)valid = false;

            now = 2;

            continue;

        }



        valid = false;

    }



    if(ct > 1 && now == 0)valid = false;

    if(ct > 1 && !have)valid = false;

    printf("%s", (valid && (mas ^ fem)) ? "YES":"NO");



    return 0;

}
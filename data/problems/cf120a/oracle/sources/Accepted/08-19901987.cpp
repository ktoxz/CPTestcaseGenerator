/********* MY GOD - _/\_ ARUNAJAY _/\_ ********/



#include<bits/stdc++.h>

using namespace std;



#define sz(c) (c).size()

#define pb push_back

#define all(c) (c).begin(), (c).end()

#define tr(c, i) for(__typeof((c).begin()) i = (c).begin(); i != (c).end(); i++)

#define present(c, x) ((c).find(x) != (c).end())

#define cpresent(c, x) (find(all(c), x) != (c).end())

#define REP(i, n) for(int i = 0; i < (n); i++)

#define REPD(i, n) for(int i = (n)-1; i >= 0; i--)

#define For(i, a, b) for(int i = (a); i <= (b); i++)

#define Ford(i, a, b) for(int i = (a); i >= (b); i--)

#define mp make_pair

#define ll long long

#define ull unsigned long long

#define modulo 1000000007

#define boostio std::ios::sync_with_stdio(false);cin.tie(NULL);

#define tt int n;cin>>n;while(n--)



int main()

{

boostio;



ifstream ifile("input.txt");

	if(ifile) freopen("input.txt","rt",stdin);

	#ifdef ONLINE_JUDGE

		if(ifile) freopen("output.txt","wt",stdout);

	#endif



string s;

int rail;



cin>>s>>rail;



if(s=="front")

{

    if(rail==1)

    {

       cout<<"L"<<endl;

    }

    else

    {

        cout<<"R"<<endl;

    }

}

else

{

    if(rail==1)

    {

        cout<<"R"<<endl;

    }

    else

    {

        cout<<"L"<<endl;

    }

}



}
#include <bits/stdc++.h>

using namespace std;

typedef long long int ll;
typedef long double ld;

typedef pair<ll, ll> ii;
typedef vector<ll> vi;
typedef vector<pair<ll, ll> > vii;
# define M_PI           3.14159265358979323846 
#define PB push_back

#define FOR(prom,a,b) for ( ll prom = (a); prom < (b); ++prom )
#define F(a) FOR(i,0,a)
#define FF(a) FOR(j,0,a)

#define MM(co, cim) memset( (co), (cim), sizeof((co)) )
#define DEB(x) cerr << ">>> " << #x << " : " << x << endl;

#define EPS (1e-10)
#define INF (1<<30)
struct PC{
    int S, R, H, C, pos;
};
int main(){
	int N,S, R, H, C;
    cin>>N;
    vector<PC> v;
    F(N){
        cin>>S>>R>>H>>C;
        PC tmp={S, R, H, C, i+1};
        v.PB(tmp);
    }

    F(N){
        FF(N){
            if(v[i].S<v[j].S &&v[i].R<v[j].R &&v[i].H<v[j].H){
                v[i].C=INF;
            }
        }
    }
    int mmin=INF;
    int p=0;
    F(N){
        if(v[i].C<mmin){
            mmin=v[i].C;
            p=i;
        }
    }
    cout<<p+1<<endl;


	return 0;
}
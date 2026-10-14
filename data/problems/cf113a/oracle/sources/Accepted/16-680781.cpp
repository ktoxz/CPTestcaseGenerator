#include <iostream>
#include <algorithm>
#include <cmath>
#include <ctime>
#include <vector>
#include <memory.h>
#include <cstdio>
#include <assert.h>
#include <map>
#include <set>
#include <queue>

using namespace std;

typedef long long ll;
typedef long double ld;

typedef vector <int> vi;
typedef vector <bool> vb;
typedef vector <double> vd;

typedef vector <vi> vvi;
typedef vector <vb> vvb;
typedef vector <vd> vvd;

#define pr pair
#define vc vector

#define pb push_back
#define mp make_pair

#define e1 first
#define e2 second

#define bgn begin
#define all(x) (x).begin(),(x).end()

#define upb upper_bound
#define lob lower_bound

#define fnd find
#define ers erase
#define ins insert
#define sz size

#define loop(i,n) for(int i = 0; i < (n); ++i)
#define loopr(i,n) for(int i = (n) - 1; i >= 0; --i)

#define lpab(i,a,b) for(int i = a; i <= b; ++i)
#define lpabr(i,a,b) for(int i = b; i >= a; --i)

#define tr(i,x) for(__typeof((x).begin()) i = (x).begin(); i != (x).end(); ++i)
#define trr(i,x) for(__typeof((x).rbegin()) i = (x).rbegin(); i != (x).rend(); ++i)

#define dbg(x) for(__typeof((x).begin()) i = (x).begin(); i != (x).end(); ++i) cerr << *i << " "; cout << endl;
#define dbgr(x) for(__typeof((x).rbegin()) i = (x).rbegin(); i != (x).rend(); ++i) cerr << *i << " "; cout << endl;

const ld eps = 1e-8;
#define inf 1000000000

#define EQ(a,b) (fabs( a - b ) < eps)
#define LS(a,b) (a < b - eps)
#define GR(a,b) (a > b + eps)

#define LSEQ(a,b) ( a < b + eps )
#define GREQ(a,b) ( a > b - eps )

typedef int elem;
#define elem_null 0
#define elem_inf  1000000000

#define getrand ( (RAND_MAX < 1000000000)?(rand() * rand()):(rand()) )

struct pt
{
    ld x, y;
    pt(){}
    pt(ld _x, ld _y): x(_x), y(_y){}

    pt operator + (const pt &p)const {return pt( x + p.x, y + p.y );}
    pt operator - (const pt &p)const {return pt( x - p.x, y - p.y );}
    pt operator * (ld c)const {return pt( x * c, y * c );}
    pt operator / (ld c)const {return pt( x / c, y / c );}

    void operator += (const pt &p) {x += p.x; y += p.y;};
    void operator -= (const pt &p) {x -= p.x; y -= p.y;};
    void operator *= (ld c) {x *= c; y *= c;};
    void operator /= (ld c) {x /= c; y /= c;};

    ///vect
    ld operator / (const pt &p)const {return ( x * p.y - y * p.x );}
    ///scalar
    ld operator * (const pt &p)const {return ( x * p.x + y * p.y );}

    ld length(){return sqrtl( x * x + y * y );}
    ld angle(){return atan2( y, x );}
};

struct treap
{
    int key, p, cnt;
    treap *l, *r;
    treap(int _key): key(_key), p(getrand), cnt(1), l(NULL), r(NULL){}
};

int getcnt (treap *t)
{
    if (t) return t->cnt;
    return 0;
}

treap* upd (treap *t)
{
    if (!t) return t;
    t->cnt = 1 + getcnt(t->l) + getcnt(t->r);
}

void split (treap *t, int key, treap *&l, treap *&r)
{
    if (!t) return void(l = r = NULL);
    if (t->key < key)
        split( t->l, key, l, t->l ), r = t;
    else
        split( t->r, key, t->r, r ), l = t;
    upd(t);
}

treap* merge (treap *l, treap *r)
{
    if (!l || !r)
        return max( l, r );
    if (l->p > r->p)
    {
        l->r = merge( l->r, r );
        return upd(l);
    }
    else
    {
        r->l = merge( l, r->l );
        return upd(r);
    }
}

struct rmq
{
    int l, r, MaxInd;
    elem Max, Add;
    rmq *L, *R;
    rmq(int b, int e)
    {
        l = b; r = e;
        MaxInd = l;
        Max = Add = elem_null;
        if (b != e)
        {
            L = new rmq( b, (b + e) / 2 );
            R = new rmq( (b + e) / 2 + 1, e );
        }
    }
    void SET (int i, elem x)
    {
        if (l == r)
            Max = x;
        else
        {
            if (i <= L->r)
                L->SET( i, x );
            else
                R->SET( i, x );
            Max = max( L->Max + L->Add, R->Max + R->Add );
            if (Max == L->Max + L->Add)
                MaxInd = L->MaxInd;
            else
                MaxInd = R->MaxInd;
        }
    }
    void ADD (int b, int e, elem x)
    {
        if (b > r || e < l)
            return;
        if (b <= l && e >= r)
            Add += x;
        else
        {
            L->ADD( b, e, x);
            R->ADD( b, e, x);
            Max = max( L->Max + L->Add, R->Max + R->Add );
            if (Max == L->Max + L->Add)
                MaxInd = L->MaxInd;
            else
                MaxInd = R->MaxInd;
        }
    }
    elem MAX (int b, int e)
    {
        if (b > r || e < l)
            return -elem_inf;
        if (b <= l && e >= r)
            return Max + Add;
        else
        {
            return max( L->MAX( b, e ), R->MAX( b, e ) ) + Add;
        }
    }
    pr<elem, int> MAX_IND (int b, int e)
    {
        if (b > r || e < l)
            return mp( -elem_inf, -elem_inf );
        if (b <= l && e >= r)
            return mp( Max + Add, MaxInd );
        else
        {
            pr<elem, int> ans = max( L->MAX_IND( b, e ), R->MAX_IND( b, e ) );
            ans.e1 += Add;
            return ans;
        }
    }
};

#define P 0
#define S 1
#define G 2

#define M 0
#define W 1

int main ()
{
    //freopen("Ainput.txt", "r", stdin);
    //freopen("Aoutput.txt", "w", stdout);

    string s;
    vector <int> t, r;
    while (cin >> s)
    {
        int was = t.sz();

        if ( s.sz() >= 4 && s.substr( s.sz() - 4, 4 ) == "lios" )
            t.pb(P), r.pb(M);
        if ( s.sz() >= 5 && s.substr( s.sz() - 5, 5 ) == "liala" )
            t.pb(P), r.pb(W);

        if ( s.sz() >= 3 && s.substr( s.sz() - 3, 3 ) == "etr" )
            t.pb(S), r.pb(M);
        if ( s.sz() >= 4 && s.substr( s.sz() - 4, 4 ) == "etra" )
            t.pb(S), r.pb(W);

        if ( s.sz() >= 6 && s.substr( s.sz() - 6, 6 ) == "initis" )
            t.pb(G), r.pb(M);
        if ( s.sz() >= 6 && s.substr( s.sz() - 6, 6 ) == "inites" )
            t.pb(G), r.pb(W);

        if (was == t.sz())
        {
            cout << "NO" << endl;
            return 0;
        }
    }

    if (t.sz() == 1)
    {
        cout << "YES" << endl;
        return 0;
    }

    for (int i = 1; i < t.sz(); ++i)
        if (r[i] != r[0])
        {
            cout << "NO" << endl;
            return 0;
        }

    int num = 0;
    for (int i = 0; i < t.sz(); ++i)
    {
        num += (t[i] == S);
    }

    if (num != 1)
    {
        cout << "NO" << endl;
        return 0;
    }

    for (int i = 0; i < t.sz() - 1; ++i)
        if (t[i] > t[i + 1])
        {
            cout << "NO" << endl;
            return 0;
        }

    cout << "YES" << endl;
    return 0;
}
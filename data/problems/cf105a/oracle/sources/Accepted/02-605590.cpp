#include <cstdio>
#include <cstring>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <vector>

using namespace std;

typedef pair<string, int> si;

vector<si> v;
int n, m, k1, k2, k;
int skill[32];
set<string> M;
char nome[32];
string nominh[32];

int main() {

    scanf("%d %d %d.%d",&n,&m,&k1,&k2);
    k = k2;
    M.clear();
    for (int i=0;i<n;i++) {
        scanf("%s %d",nome,&skill[i]);
        string t= nome;
        M.insert(t);
        nominh[i] = t;
    }
    v.clear();
    for (int i=0;i<n;i++) {
        int a = (k*skill[i])/100;
        if (a >= 100)
            v.push_back(si(nominh[i],a));
        else {
            string t = nominh[i];
            M.erase(t);
        }
    }

    for (int i=0;i<m;i++) {
        scanf("%s",nome);
        string t = nome;
        if (M.find(t) == M.end()) {
            v.push_back(si(t,0));
        }
    }
    sort(v.begin(),v.end());
    printf("%d\n",(int)v.size());
    for (int i=0;i<(int)v.size();i++) {
        printf("%s %d\n",v[i].first.c_str(),v[i].second);
    }

    return 0;
}
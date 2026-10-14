#include <bits/stdc++.h>
#define AUTOTEST_
#ifdef AUTOTEST
    #include "autotest.h"
#endif

using namespace std;

vector<string> split(string s, string border);

#define int long long
#define double long double
#define make(type, n) type n; cin >> n
#define ALL(x) (x).begin(), (x).end()
#define FORIT(p) for(auto it = p.begin(); it != p.end(); it++)
#define FOR(i, count) for(int i = 0; i < (count); i++)
#define FORE(i, l, r) for(int i = (l); i < (r); i++)
#define NFOR(i, n) for(int i = (((int) n)-1); i >= 0; i--)
#define VI vector<int>
#define VVI vector<vector<int>>
#define PII pair<int, int>
#define makev(a, n) VI a(n); FOR(i, n) cin >> a[i];
#define get_bit(mask, pos) ((mask >> pos) & 1)
#define set_bit_0(mask, pos) (mask &= (~(1 << pos)))
#define set_bit_1(mask, pos) (mask |= (1 << pos))
#define sqrt(x) sqrtl(x)
#define dis(x1, y1, x2, y2) hypotl((x2-x1), (y2-y1))
#define sqr(x) ((x)*(x))
#define correct(x, y, xmax, ymax) ((x) >= 0 && (x) < (xmax) && (y) >= 0 && (y) < (ymax))

struct node{
    node(int id){
        this->id = id;
    }

    vector<node*> child;
    node* parent;

    int size_subtree;
    int pos_in_array;
    int id;

    void calc_size(){
        size_subtree = 1;
        FOR(i, child.size()){
            child[i]->calc_size();
            size_subtree += child[i]->size_subtree;
        }
    }

    int get_child_number(int k){
        if (k == 0) return id;
        k--;

        FOR(i, child.size()){
            if (k < child[i]->size_subtree){
                return child[i]->get_child_number(k);
            } else {
                k -= child[i]->size_subtree;
            }
        }

        return -2;
    }

    void dsu_save(VI& dsu){
        dsu.push_back(id);
        pos_in_array = dsu.size()-1;

        FOR(i, child.size()){
            child[i]->dsu_save(dsu);
        }
    }
};

void solve(){
    make(int, n);
    make(string, a);
    make(string, b);

    multiset<char> f;
    f.insert('a');
    f.insert('a');

    int ans = 0;
    FOR(i, n/2) {
        multiset<char> c;
        c.insert(a[i]);
        c.insert(a[n - i - 1]);
        c.insert(b[i]);
        c.insert(b[n - i - 1]);

        set<char> c2;
        c2.insert(a[i]);
        c2.insert(a[n - i - 1]);
        c2.insert(b[i]);
        c2.insert(b[n - i - 1]);

        if (c2.size() == 2) {
            if (c.count(a[i]) != 2) ans++;
        }
        if (c2.size() == 3) {
            if (a[i] == a[n-i-1]) ans++;
            ans++;
        }
        if (c2.size() == 4) ans+=2;


        //cerr << "Size: " << c2.size() << "; Ans: " << ans << endl;
    }

    if (n%2 == 1){
        cerr << a[n/2] << " == " << b[n/2] << endl;
        if (a[n/2] != b[n/2]) ans++;

        cerr << "Ans: " << ans;
    }

    cout << ans;
}



/*
VI D;

void solve(){
    make(int, n);
    make(int, m);

    D = VI(1e6);
    FOR(i, 1e6) D[i] = 0;

    FORE(i, 1, 1e6){
        int pos = i;
        while (pos < 1e6){
            D[pos]++;
            pos += i;
        }
    }

    cerr << D[2] << endl;
    cerr << D[4] << endl;
    cerr << D[7] << endl;
    cerr << D[17] << endl;
    cerr << D[100] << endl;
    cerr << D[97] << endl;
    cerr << D[52342] << endl;
}
*/
/*
int INF = 10e16;

struct node{

    node(int id){
        this->id = id;
    }

    vector<node*> links;
    vector<int> price;

    int id;
    int price_node;
};

void solve(){
    make(int, n);
    make(int, m);

    vector<node*> graph(n);
    FOR(i, n) graph[i] = new node(i);

    FOR(i, m){
        make(int, u);
        make(int, v);
        make(int, p);

        graph[u-1]->links.push_back(graph[v-1]);
        graph[u-1]->price.push_back(p);

        graph[v-1]->links.push_back(graph[u-1]);
        graph[v-1]->price.push_back(p);
    }

    FOR(i, n){
        make(int, a);
        graph[i]->price_node = a;
    }


}
*/

/*
string tobit(string s) {
    string t = "";
    FOR(i, s.length()) {
            if (s[i] == '0') t += "0000";
            if (s[i] == '1') t += "0001";
            if (s[i] == '2') t += "0010";
            if (s[i] == '3') t += "0011";
            if (s[i] == '4') t += "0100";
            if (s[i] == '5') t += "0101";
            if (s[i] == '6') t += "0110";
            if (s[i] == '7') t += "0111";
            if (s[i] == '8') t += "1000";
            if (s[i] == '9') t += "1001";
            if (s[i] == 'A') t += "1010";
            if (s[i] == 'B') t += "1011";
            if (s[i] == 'C') t += "1100";
            if (s[i] == 'D') t += "1101";
            if (s[i] == 'E') t += "1110";
            if (s[i] == 'F') t += "1111";
    }
    return t;
}

void solve() {
    make(int, n);
    make(int, m);

    VI prev_line(m);
    VI now_line(m);
    FOR(i, m) now_line[i] = 0;

    int count = 0;
    int del = 0;
    FOR(number_line, n){
        make(string, s);
        string line = tobit(s);

        FOR(i, m){
            prev_line[i] = now_line[i];
            now_line[i] = 0;
        }


        map<int, int> change;
        FOR(i, m){
            if (prev_line[i] != 0){
                if (change.count(prev_line[i]) == 0) {
                    change[prev_line[i]] = change.size() + 1;
                }

                prev_line[i] = change[prev_line[i]];
            }
        }


        int start = -1;
        set<int> old_numbers;
        FOR(i, m){
            if (line[i] == '1'){
                if (start == -1) start = i;

                if (i > 0 && now_line[i-1] != 0){
                    now_line[i] = now_line[i-1];
                } else {
                    count++;
                    now_line[i] = count;
                }

                if (prev_line[i] != 0){
                    old_numbers.insert(prev_line[i]);
                }
            } else {
                if (start == -1) continue;

                if (old_numbers.size() > 0) {
                    FORE(pos, start, i) {
                        now_line[pos] = *(old_numbers.begin());
                    }

                    FORIT(old_numbers){
                        FORE(pos, 0, m){
                            if (prev_line[pos] == *it) prev_line[pos] = *(old_numbers.begin());
                        }
                    }
                }

                start = -1;
                del += old_numbers.size();
                old_numbers.clear();
            }
        }

        //-----------
        if (old_numbers.size() > 0) {
            FORE(pos, start, m) {
                now_line[pos] = *(old_numbers.begin());
            }

            FORIT(old_numbers){
                FORE(pos, 0, m){
                    if (prev_line[pos] == *it) prev_line[pos] = *(old_numbers.begin());
                }
            }
        }

        del += old_numbers.size();
    }

    cout << count-del;
}
*/

signed main(signed argc, char* argv[]) {
#ifdef AUTOTEST
    autotest tests(&solve);
    return 0;
#endif

    ios_base::sync_with_stdio(0);
    cin.tie();

    if (argc > 1 && (string) argv[1] == "file") {
        freopen("input.txt", "r", stdin);
        freopen("output.txt", "w", stdout);

        int number_sample = 1;
        do {
            cout << "Sample #" << number_sample << ":" << endl;
            cerr << "Sample #" << number_sample << ":" << endl;

            solve();
            number_sample++;

            cout << endl;
            cerr << endl;
        } while (!cin.eof());
    } else {
        cerr.clear(ios_base::badbit);
        solve();
    }
}

vector<string> split(string s, string border){
    vector<string> ans;
    int pos_end;

    while((pos_end = s.find(border)) != string::npos){
        if (pos_end) ans.push_back(s.substr(0, pos_end));
        s = s.substr(pos_end + border.size());
    }

    return ans;
}
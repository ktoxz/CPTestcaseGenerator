/*
 * Author: FreeIdea
 * Created Time:  2011/8/19 23:11:18
 * File Name: B.cpp
 */
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <algorithm>
#include <vector>
using namespace std;
const int maxint = -1u>>1;
template <class T> bool get_max(T& a, const T &b) {return b > a? a = b, 1: 0;}
template <class T> bool get_min(T& a, const T &b) {return b < a? a = b, 1: 0;}

struct Lap {
    int a, b, c, d;
    bool operator > (const Lap &A) const {
        if(a > A.a && b > A.b && c > A.c)   return true;
        return false;
    }
}lap[105];

int n;
bool cs[105];

int main() {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) {
        scanf("%d%d%d%d", &lap[i].a, &lap[i].b, &lap[i].c, &lap[i].d);
    }
    memset(cs, true, sizeof(cs));
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            if(i != j) {
                if(lap[j] > lap[i]) {
                    cs[i] = false;
                }
            }
        }
    }
    int ans = maxint, id;
    for(int i = 0; i < n; i++) {
        if(cs[i]) {
            if(get_min(ans, lap[i].d)) {
                id = i + 1;
            }
        }
    }
    printf("%d\n", id);
    return 0;
}
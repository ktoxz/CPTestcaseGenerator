#include <cstdio>

//By chyx111
#define Rep(i,n) for(int n_ = (n), i = 0; i< n_; ++i)

int main() {
    int n; 
    while( scanf("%d", &n) == 1 ){
        bool found = false;
        for(int n4 = 0; n4 * 4 <= n; ++n4){
            if( (n - n4 * 4) % 7 == 0 ){
                found = true;
                Rep(i, n4)putchar('4');
                Rep(i, (n-n4*4)/7)putchar('7');
                puts("");
                break;
            }
        }
        if( !found ){
            puts("-1");
        }
    }
    return 0;
}
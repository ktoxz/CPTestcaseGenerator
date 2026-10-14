#include <stdio.h>

int dec(char c){
	switch(c){
	case '6': return 6;
	case '7': return 7;
	case '8': return 8;
	case '9': return 9;
	case 'T': return 10;
	case 'J': return 11;
	case 'Q': return 12;
	case 'K': return 13;
	case 'A': return 15;
	}
}

int istrump(char trump,char this){
	if(trump==this)return 1;
	else return 0;
}

int main(void)
{
        char a,b,c,d,e;
        int scorea,scoreb;
        int win;
        scanf(" %c",&a);
        //fflush(stdin);
        scanf(" %c%c %c%c",&b,&c,&d,&e);
        if(istrump(a,c)){
                if(istrump(a,e)){
                        if(dec(b)>=dec(d))win=1;
                        else win=0;
                }
                else win=1;
        }
        else{
                if(c==e){
                        if(dec(b)>=dec(d))win=1;
                        else win=0;
                }
                else if(istrump(a,e)){
                        win=0;
                }
                else win=0;
        }
       
        if(win)puts("YES");
        else puts("NO");
       
        return 0;
}
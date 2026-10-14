#include<stdio.h>
int main(void)
{
	int a,h,hr,m;
	scanf("%d:%d",&h,&m);
	hr=(h%10)*10+(h/10);
	if(hr>m && hr<60)
	{
            printf("%02d:%02d\n",h,hr);
            }
 else
 {
	 h++;
	 h=h%24;
	 hr=(h%10)*10+(h/10);
	 while(hr>=60)
	 {
	 h++;
	 h=h%24;
	 hr=(h%10)*10+(h/10);
	 }
     printf("%02d:%02d\n",h,hr);
     }
    return 0;
}
#include<stdio.h>

int main()
{
    long int a = 456;
    double b;
    b = a/1000000.0;

    printf("%06ld\n",a);
    printf("%f\n",b);

    return 0;
}

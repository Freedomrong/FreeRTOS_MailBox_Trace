/*************************************************************************
	> File Name: timestamp.c
    > Function: 时间戳
	> Author: 
	> Mail: 
	> Created Time: 2018年11月24日 星期六 17时56分07秒
 ************************************************************************/

#include<stdio.h>
#include<sys/time.h>
#include<time.h>
#include<unistd.h>
#include<stdlib.h>

int main()
{
   /*Unix年月日十分秒*/
    time_t t;
    struct tm * lt;
    time(&t);
    lt = localtime(&t);

    char * argv[] = {"pulseview"};

    struct timeval tv;
    gettimeofday(&tv, NULL);

    // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
    printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",lt->tm_year+1900, lt->tm_mon+1, lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec, tv.tv_usec);

    system(*argv);

    return 0;
   
}

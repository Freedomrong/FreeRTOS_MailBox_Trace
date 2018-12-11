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

typedef struct Time_Stamp
{
    struct tm * lt;
    struct timeval tv;
}timestamp;

timestamp Print_Timestamp();

int main()
{
  // /*Unix年月日十分秒*/
  //  time_t t;
  //  struct tm * lt;
  //  time(&t);
  //  lt = localtime(&t);

  //  char * argv[] = {"pulseview"};

  //  struct timeval tv;
  //  gettimeofday(&tv, NULL);

  //  // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
  //  printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",lt->tm_year+1900, lt->tm_mon+1, lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec, tv.tv_usec);

  //  system(*argv)
    Print_Timestamp();
    return 0;
   
}


timestamp Print_Timestamp()
{
   /*Unix年月日十分秒*/
    time_t t;
    //struct tm * lt;
    timestamp Ts;

    time(&t);

    Ts.lt = localtime(&t);

    char * argv[] = {"pulseview"};

    //struct timeval tv;
    gettimeofday(&(Ts.tv), NULL);

    // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
    printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",Ts.lt->tm_year+1900, Ts.lt->tm_mon+1, Ts.lt->tm_mday, Ts.lt->tm_hour, Ts.lt->tm_min, Ts.lt->tm_sec, Ts.tv.tv_usec);

    system(*argv);

    return Ts;
   
}

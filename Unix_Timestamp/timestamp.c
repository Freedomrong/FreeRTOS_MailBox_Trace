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

    struct timeval tv;
    gettimeofday(&tv, NULL);

    // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
    printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",lt->tm_year+1900, lt->tm_mon+1, lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec, tv.tv_usec);
    return 0;
   
   /*Unix秒数.微秒数*/ 
  // struct timeval start, end;
  // gettimeofday(&start, NULL);
  // printf("start : %d.%d\n", start.tv_sec, start.tv_usec);
  // sleep(1);
  // gettimeofday(&end, NULL);
  // printf("end   : %d.%d\n", end.tv_sec, end.tv_usec);
  // return 0;
    
  // struct timeval tv;
  // gettimeofday(&tv, NULL);
  // printf("second:%ld\n",tv.tv_sec);  //秒
  // printf("millisecond:%ld\n",tv.tv_sec*1000 + tv.tv_usec/1000);  //毫秒
  // printf("microsecond:%ld *1000000 + %ld\n",tv.tv_sec, tv.tv_usec);  //微秒

  // sleep(3); //睡眠3秒
  // printf("3s later");

  // gettimeofday(&tv, NULL);
  // printf("second:%ld\n",tv.tv_sec);  //秒
  // printf("millisecond:%ld\n",tv.tv_sec*1000 + tv.tv_usec/1000);  //毫秒
  // printf("microsecond:%ld *1000000 + %ld\n",tv.tv_sec, tv.tv_usec);  //微秒

   
}

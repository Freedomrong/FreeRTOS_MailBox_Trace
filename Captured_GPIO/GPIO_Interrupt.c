/*************************************************************************
	> File Name: GPIO_Interrupt.c
	> Author: 
	> Mail: 
	> Created Time: 2018年12月10日 星期一 16时55分04秒
 ************************************************************************/

#include<stdio.h>
#include<stdlib.h>
#include<wiringPi.h>
#include<time.h>
#include<unistd.h>
#include<sys/time.h>


#define PinRising_input 1       // wiringPi只能控制0到16号的GPIO
#define PinFalling_input 4 

#define Pin_output 6

// 写一个链队列结构把时间戳保存下来，采集结束后统一写入文件


// 写一个时间戳结构
typedef struct Time_Stamp
{
    struct tm * lt;
    struct timeval tv;

}timestamp;

// 定义一个中断计数变量
static volatile int switch_count = 0;

/**************************
    > 时间戳获取函数
**************************/
timestamp Get_Timestamp()
{
   /*Unix年月日十分秒*/
    time_t t;
    timestamp Ts;
    time(&t);
    Ts.lt = localtime(&t);
    gettimeofday(&(Ts.tv), NULL);

    // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月
    //printf("c timestamp: %d/%d/%d %d:%d:%d.%ld\n",Ts.lt->tm_year+1900, Ts.lt->tm_mon+1, Ts.lt->tm_mday, Ts.lt->tm_hour, Ts.lt->tm_min, Ts.lt->tm_sec, Ts.tv.tv_usec);

    return Ts;
}


/**************************
    > 中断处理函数
**************************/
void LED(void)
{
    // printf("enter interrupt");
    switch_count = switch_count + 1;
    
    if(switch_count == 1)
    {
        digitalWrite(Pin_output, HIGH);
        Get_Timestamp();
    }

    if(switch_count == 2)
    {
        digitalWrite(Pin_output, LOW);
        switch_count = 0;
    }

}

void Setup(void)
{

    if(wiringPiSetup() == -1) //wiringPiSetupGpio()表示使用GPIO编号，wiringPiSetup()则使用物理编号
    {
        printf("Setup wiringPi failed!");
    }

    pinMode(PinRising_input, INPUT);
    pullUpDnControl(PinRising_input, PUD_UP);

    pinMode(PinFalling_input, INPUT);
    pullUpDnControl(PinFalling_input, PUD_UP);

    pinMode(Pin_output, OUTPUT);

}


int main (void)
{

    Setup();

    if(wiringPiISR(PinRising_input, INT_EDGE_RISING, LED) < 0)
    {
        printf("Regist PinRising_input interrupts failed!");
        return -2;
    }

    if(wiringPiISR(PinFalling_input, INT_EDGE_FALLING, LED) < 0)
    {
        printf("Regist PinFalling_input interrupts failed!");
        return -2;
    }

    while(1)
    {
        ;
    } 

    return 0 ;
}


/*const int LEDpin = 1;

int main()
{
    if(-1==wiringPiSetup())
    {
        printf("setup error\n");
        exit(-1);          
    }
    pinMode(LEDpin,OUTPUT);      


    for(size_t i=0;i<10;++i)
    {
        digitalWrite(LEDpin,HIGH); 
        delay(600);
        digitalWrite(LEDpin,LOW);
        delay(600);
    }
    printf("------------bye-------------");
    return 0;   
}*/

#!/usr/bin/env python3
# coding=utf-8
'''
Function: 捕获FreeRtosTick中插入的GPIO翻转,Tick是周期的,GPIO以Tick为半周期(1ms)进行翻转

Author:   hujiaodigua
Date:     20181207

注意:
     这个脚本里的内容需要写在时间戳捕获的脚本里面,要能记录下来捕获数据经历了多少个Tikc(内部时间)
     因为PulseView虽然是可视化工具,可是对于编写分析脚本是没有实质性帮助的,
     
     当然还可以考虑使用sigrok-cli导入数据得到高低电平数据
     然后数它捕获的Tick的数量(这个和Raspberry Pi中断捕获哪个准确度高,有待进一步实验)
     Rasperry Pi捕获是实时的
     sigrok-cli也是先抓下来，然后再显示出来，可我们就是用到sigrok-cli抓SWO和Tick中的定期GPIO触发，而且两者的时间通过DWT_Watchpoint捕获定期GPIO进行对齐
     '''


import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD)

PinRising_input = 37
PinFalling_input = 38
Pin_output = 22

global SwitchCounter
global InterruptCounter
global HighLevelCounter
global LowLevelCounter
global Begin_Timestamp
global End_Timestamp

SwitchCounter = 0
InterruptCounter = 0
HighLevelCounter = 0
LowLevelCounter = 0
Begin_Timestamp = 0
End_Timestamp = 0

def LED(self):
    global SwitchCounter
    global InterruptCounter
    global HighLevelCounter
    global LowLevelCounter
    global Begin_Timestamp
    global End_Timestamp

    SwitchCounter = SwitchCounter + 1
    InterruptCounter = InterruptCounter + 1

    if SwitchCounter == 1:    # 上升沿/下降沿进入一次回调函数
        GPIO.output(Pin_output, GPIO.HIGH)
        HighLevelCounter = HighLevelCounter + 1
        Begin_Timestamp = datetime.datetime.now()
    
    if SwitchCounter == 2:    # 上升沿/下降沿又一次进入回调函数
        GPIO.output(Pin_output, GPIO.LOW)
        SwitchCounter = 0
        LowLevelCounter = LowLevelCounter + 1
        End_Timestamp = datetime.datetime.now()

    if InterruptCounter == 1000:
        # 进一次回调函数表示一次上升沿或一次下降沿,上升沿与下降沿的时间间隔为1ms
        print("InterruptCounter: " + str(InterruptCounter))
        
        # InterruptCounter = HighLevelCounter + LowLevelCounter
        print("HighLevelCounter: " + str(HighLevelCounter))
        print("LowLevelCounter: " + str(LowLevelCounter))

        print("Begin_Timestamp: " + str(Begin_Timestamp))
        print("End_Timestamp: " + str(End_Timestamp))

        InterruptCounter = 0
        HighLevelCounter = 0
        LowLevelCounter = 0

try:
    GPIO.setmode(GPIO.BOARD)
    # 点亮一个GPIO表示成功捕获到中断了
    GPIO.setup(Pin_output, GPIO.OUT)

    # 中断捕获引脚，用来捕获FreeRTOS的定期GPIO触发
    GPIO.setup(PinRising_input, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(PinFalling_input, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # 为什么不能对一个引脚既设定下降沿捕获又设定上升沿捕获呢,设定两个引脚感觉不灵活很死板
    GPIO.add_event_detect(PinRising_input, GPIO.RISING, callback = LED)
    GPIO.add_event_detect(PinFalling_input, GPIO.FALLING, callback = LED)

    
    while True:
        time.sleep(1)

finally:
    GPIO.cleanup()

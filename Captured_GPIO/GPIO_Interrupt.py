#!/usr/bin/env python3
# coding=utf-8
'''
Function: 捕获FreeRtosTick中插入的GPIO翻转,Tick是周期的,GPIO以Tick为半周期(1ms)进行翻转

Author:   hujiaodigua
Date:     20181207
'''


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

PinRising_input = 37
PinFalling_input = 38
Pin_output = 22

global SwitchCounter
global InterruptCounter

SwitchCounter = 0
InterruptCounter = 0
HighLevelCounter = 0
LowLevelCounter = 0

def LED(self):
    global SwitchCounter
    global InterruptCounter
    global HighLevelCounter
    global LowLevelCounter

    SwitchCounter = SwitchCounter + 1
    InterruptCounter = InterruptCounter + 1

    if InterruptCounter == 1000:
        # 进一次回调函数表示一次上升沿或一次下降沿,上升沿与下降沿的时间间隔为1ms
        print("InterruptCounter: " + str(InterruptCounter))
        
        # InterruptCounter = HighLevelCounter + LowLevelCounter
        print("HighLevelCounter: " + str(HighLevelCounter))
        print("LowLevelCounter: " + str(LowLevelCounter))

        InterruptCounter = 0
        HighLevelCounter = 0
        LowLevelCounter = 0

    if SwitchCounter == 1:    # 上升沿/下降沿进入一次回调函数
        GPIO.output(Pin_output, GPIO.HIGH)
        HighLevelCounter = HighLevelCounter + 1
    
    if SwitchCounter == 2:    # 上升沿/下降沿又一次进入回调函数
        GPIO.output(Pin_output, GPIO.LOW)
        SwitchCounter = 0
        LowLevelCounter = LowLevelCounter + 1

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

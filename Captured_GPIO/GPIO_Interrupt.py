#!/usr/bin/env python3
# coding=utf-8

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

Pin_input = 37
Pin_output = 22

global SwitchCounter
global InterruptCounter
SwitchCounter = 0
InterruptCounter = 0

def LED(self):
    global SwitchCounter
    global InterruptCounter

    SwitchCounter = SwitchCounter + 1
    InterruptCounter = InterruptCounter + 1

    if InterruptCounter == 1000:
        print("InterruptCounter: " + str(InterruptCounter))
        InterruptCounter = 0

    if SwitchCounter == 1:    # 上升沿进入一次回调函数
        GPIO.output(Pin_output, GPIO.HIGH)
    
    if SwitchCounter == 2:    # 上升沿又一次进入回调函数
        GPIO.output(Pin_output, GPIO.LOW)
        SwitchCounter = 0

try:
    GPIO.setmode(GPIO.BOARD)
    # 点亮一个GPIO表示成功捕获到中断了
    GPIO.setup(Pin_output, GPIO.OUT)

    # 中断捕获引脚，用来捕获FreeRTOS的定期GPIO触发
    GPIO.setup(Pin_input, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    GPIO.add_event_detect(Pin_input, GPIO.RISING, callback = LED)
    # 为什么不能对一个引脚既设定下降沿捕获又设定上升沿捕获呢
    
    while True:
        time.sleep(1)

finally:
    GPIO.cleanup()

#!/usr/bin/env python3
# coding=utf-8
# sys.argv[1] 是追踪数据名称
# sys.argv[2] 是记录文件名称

import time
import datetime
import os
import shutil
import subprocess
import sys
import multiprocessing

def Captured_GPIO(e):

    global file_object 
    global Capturedfile_Name 
    global Capturedfile_Format 
    global CapturedGPIO_Name 
    global CapturedGPIO_Format 
    global CapturedTimes 
    
    for i in range(0,int(CapturedTimes)):
        e.wait()
        e.clear()
        # print('wait e.is_set()--' + str(e.is_set()))
        # time.sleep(0.01)
        CapturedGPIO_Command = ("./GPIO_Interrupt " + str(i) + CapturedGPIO_Name + CapturedGPIO_Format)   
 
        response_GPIO = subprocess.getstatusoutput(CapturedGPIO_Command)  
        
def Captured_Command(e):

    global file_object 
    global Capturedfile_Name 
    global Capturedfile_Format 
    global CapturedGPIO_Name 
    global CapturedGPIO_Format 
    global CapturedTimes 
    
    for i in range(0,int(CapturedTimes)):
        e.set()
        # print('set e.is_set()--' + str(e.is_set()))
        # e.clear()
        # print('clear set e.is_set()--' + str(e.is_set()))
        CapturedCommand = ("sigrok-cli --time 100 -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2_Tick,3=CLK_Pulse -O vcd -o "\
                           + str(i) + Capturedfile_Name + Capturedfile_Format)
 
        response = subprocess.getstatusoutput(CapturedCommand)    

        print(str(i) + str(response))
        file_object.write(str(i) + Capturedfile_Name+';')
        file_object.write(str(response))
        file_object.write('\n')
        
    file_object.close();
    e.set()


if __name__ == "__main__":

    file_object = open(str(sys.argv[2]) + '.txt', 'w')
    Capturedfile_Name = '-' + str(sys.argv[1])
    Capturedfile_Format = '.vcd'
    CapturedGPIO_Name = '-GPIO_Timestamp'
    CapturedGPIO_Format = '.txt'
    CapturedTimes = sys.argv[3]
    
    e = multiprocessing.Event()
    
    task_Captured_GPIO = multiprocessing.Process(name = 'block', target = Captured_GPIO, args = (e,))
    task_Captured_Command = multiprocessing.Process(name = 'block', target = Captured_Command , args = (e,))

    task_Captured_GPIO.start()
    task_Captured_Command.start()

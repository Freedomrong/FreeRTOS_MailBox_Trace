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

file_object = open(str(sys.argv[2]) + '.txt', 'w')

#Capturedfile_Name = 'MailBox_tracing.sr'
Capturedfile_Name = '-' + str(sys.argv[1])
Capturedfile_Format = '.vcd'

for i in range(0,10):
    begin = datetime.datetime.now();
    print(str(i) + " begin timestamp: ", begin)

    #subprocess.call("sigrok-cli --time 50 -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -o MailBox_tracing.sr", shell = True)
    subprocess.call("sigrok-cli --samples 500k -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -O vcd -o "+ str(i) + Capturedfile_Name + Capturedfile_Format, shell = True)
    #subprocess.call("sigrok-cli --samples 500k -d fx2lafw -c samplerate=24MHz -C 0=SWO -O vcd -o "+ str(i) + Capturedfile_Name + Capturedfile_Format, shell = True)

    end = datetime.datetime.now();
    print(str(i) + " end time stamp", end)
    print('*****************************')

    file_object.write(str(i) + Capturedfile_Name+';')
    file_object.write(str(begin) + ';')
    file_object.write(str(end) + ';')
    file_object.write('\n')

    time.sleep(0.000001) # 休眠1us

    #捕获这个shell命令要内嵌进来
    #sigrok-cli -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -o MailBox_tracing.vcd --time 50

file_object.close();

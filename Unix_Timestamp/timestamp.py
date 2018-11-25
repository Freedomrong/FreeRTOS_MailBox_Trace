#!/usr/bin/env python3
# coding=utf-8

import time
import datetime
import os
import shutil
import subprocess

#Capturedfile_Name = 'MailBox_tracing.sr'
Capturedfile_Name = 'MailBox_tracing.vcd'

begin = datetime.datetime.now();
print("python timestamp: ", begin)

#subprocess.call("sigrok-cli --time 50 -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -o MailBox_tracing.sr", shell = True)
subprocess.call("sigrok-cli --time 50 -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -O vcd -o "+Capturedfile_Name, shell = True)

end = datetime.datetime.now();
print("end time stamp", end)

file_object = open('Data&Timestamp_mark.txt', 'w')
file_object.write(Capturedfile_Name+';')
file_object.write(str(begin)+';')
file_object.write(str(end)+';')
#捕获这个shell命令要内嵌进来
#sigrok-cli -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -o MailBox_tracing.vcd --time 50

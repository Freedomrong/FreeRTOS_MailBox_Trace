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

def Captured_Function():

    file_object = open(str(sys.argv[2]) + '.txt', 'w')
    
    # Capturedfile_Name = 'MailBox_tracing.sr'
    Capturedfile_Name = '-' + str(sys.argv[1])
    Capturedfile_Format = '.vcd'
    # Capturedfile_Format = '.sr'
    
    
    CapturedTimes = sys.argv[3]
    
    for i in range(0,int(CapturedTimes)):
        # begin = datetime.datetime.now();
        # print(str(i) + " begin timestamp: ", begin)
       
        # CapturedCommand = ("sigrok-cli --samples 1M -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2_Tick,3=CLK_Pulse -o "\
        #                    + str(i) + Capturedfile_Name + Capturedfile_Format)
    
        # CapturedCommand = ("sigrok-cli --samples 1M -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2_Tick,3=CLK_Pulse -O vcd -o "\
        #                    + str(i) + Capturedfile_Name + Capturedfile_Format)
    
        CapturedCommand = ("sigrok-cli --time 10 -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2_Tick,3=CLK_Pulse -O vcd -o "\
                           + str(i) + Capturedfile_Name + Capturedfile_Format)
    
        response = subprocess.getstatusoutput(CapturedCommand)    # 返回的数据中有时间戳信息,是捕获数据的0时刻对应的unix时间,
                                                                  # 是我们修改sigrok-cli的源代码得到的
                                                                  # subprocess.call不能获得返回值
    
        print(str(i) + str(response))
    
        # end = datetime.datetime.now();
        # print(str(i) + " end time stamp", end)
        # print('*****************************')
    
        file_object.write(str(i) + Capturedfile_Name+';')
        # file_object.write(str(begin) + ';')
        # file_object.write(str(end) + ';')
        file_object.write(str(response))
     
        file_object.write('\n')
    
        # time.sleep(0.000001) # 休眠1us
    
        # 捕获这个shell命令要内嵌进来
        # sigrok-cli -d fx2lafw -c samplerate=24MHz -C 0=SWO,1=LED0,2=LED2 -o MailBox_tracing.vcd --time 50
    
    file_object.close();


if __name__ == "__main__":
    Captured_Function();

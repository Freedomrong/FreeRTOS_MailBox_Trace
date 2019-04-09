#!/usr/bin/env python3
# coding=utf-8
'''
运行脚本前记得运行一下pluseview或sigrok-cli保证固件上传
使用arm-none-eabi-gdb -q -x script.py xx.elf 
'''
import gdb
import time
import datetime
import os
import shutil
import subprocess
import sys
import multiprocessing
import usb.core
import usb.util
from vcd import VCDWriter


def Captured_GPIO(e):
    
    # global file_object 
    # global Capturedfile_Name 
    # global Capturedfile_Format 
    # global CapturedGPIO_Name 
    # global CapturedGPIO_Format 
    global CapturedTimes 
    
    # gdb.execute('target remote localhost:3333')
    # gdb.execute('monitor reset')
    # gdb.execute('monitor halt')
    # gdb.execute('load')

    for i in range(0,int(CapturedTimes)):
        e.wait()
       #  e.set()

        time.sleep(0.25)    # 把USB传输数据前的那段时间等过去,不能让GPIO的中断捕获跑到USB传输前面去
        # gdb.execute('monitor resume')


        # e.clear()
        # print('wait e.is_set()--' + str(e.is_set()))
        # time.sleep(0.01)
        # CapturedGPIO_Command = ("./GPIO_Interrupt " + str(i) + CapturedGPIO_Name + CapturedGPIO_Format) 
        # CapturedGPIO_Command = ("./GPIO_Interrupt " + "mailbox_timestamp.txt")

        # response_GPIO = subprocess.getstatusoutput(CapturedGPIO_Command)  
        os.system('./GPIO_Interrupt mailbox_timestamp.txt ')     # 把这一句放到USB采集脚本里面:执行,毕竟GPIO捕获是可以等待信号到来进行捕获



def USB_Sample(e):
    # 先开pulseview保证fx2有固件
    
    # find our device
    dev = usb.core.find(idVendor=0x0925, idProduct=0x3881)
    
    # was it found?
    if dev is None:
        raise ValueError('Device not found')
    
    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()
    # print('===============================')
    # print(dev)
    
    # get an endpoint instance
    cfg = dev.get_active_configuration()
    # print('===============================')
    # print(cfg)
    
    intf = cfg[(0,0)]
    # print('===============================')
    # print(intf)
    
    ret = dev.ctrl_transfer(0xc0,0xb0,0,0,0x02,0x00)
    # print(ret)
    
    # time.sleep(1)
    ret = dev.ctrl_transfer(0xc0,0xb2,0,0,0x01,0x00)
    # print(ret)
    
    # time.sleep(1)
    
    # 计算采样率
    samplerate = 24000000 # 可设定的采样率
    
    SR_48MHz = 48000000
    SR_30MHz = 30000000
    
    delay = 0
    flags = 0
    delay_h = 0
    delay_l =0
    
    if (SR_48MHz % samplerate == 0):
        flags = 0x40
        delay = int(SR_48MHz / samplerate -1)
        if delay > ( 6*256 ):
            delay = int(0)
    
    if (delay == 0) and ((SR_30MHz % samplerate) == 0):
        flags = 0x00
        delay = int(SR_30MHz / samplerate - 1)
    
    delay_h = delay & 0xff00
    delay_l = delay & 0x00ff
    
    
    Setdata = [flags,delay_h,delay_l]
    
    # print(ret)
    
    # 读取数据的字节数决定了采集的时长
    # 读取数据 4096*2048 = 8388608字节
    # samples = 4096*2048 # 捕获的字节数，只能是2的幂次方(最少是512)，1个字节是8bit就是8个通道，例如1024个字节代表一个通道1024个点，总共1024*8个点,目前的interface最大字节数是4096*2048
    samples =  4096*128*2*8 # ,在24MHz下这个数字最小是512，比这个还小就会卡死
                            # 4096*128*2是45ms时间
                            # 在raspberry上，fx2lafw-0.1.6的固件版本这里能设定的最大采样点数是4096*128*2*8为360ms,得到的文件大小为72MB
    
    # 本来是先读一次，使buf不为空，但是多次读取就目前的程序写法而言会造成数据的丢失，所以还是改为一次读取了
    # begin_unixtimestamp = time.time()
    ret = dev.ctrl_transfer(0x40,0xb1,0,0,Setdata,0x0300)
    
    begin_transtimestamp = time.time()
    # 这里需要记录一下unix时间戳,捕获360ms的数据在读取USB阶段大约总共需要花费380ms
    e.set()
    buf = intf[0].read(samples)
    # e.set()
    # end_sample_unixtimestamp = time.time()
    # print(begin_unixtimestamp)

    print('USB读取数据前的时间戳为')
    print(begin_transtimestamp)

    # print(end_sample_unixtimestamp)
    
    # buf_output = buf.tolist()
    # print(buf)
    filename = 'mailbox_samples.txt'
    file_object = open(filename,'w')
    
    for i in range(0,len(buf)):
        file_object.write(bin(buf[i]).replace('0b',''))
        file_object.write('\n')
    
    file_object.close()



def GDB_Command(e):
    
    gdb.execute('target remote localhost:3333')
    gdb.execute('monitor reset')
    gdb.execute('monitor halt')
    gdb.execute('load')
    
    e.set()    # 这个进程走到这里再去控制另外两个进程开始采集
    gdb.execute('monitor resume')

    # e.wait()
    # print('GDB_Command运行了')
    # response = subprocess.getstatusoutput('arm-none-eabi-gdb -q -x gdb_script.py MailBox.elf') # 只要GDB运行了，USB读取进程必然变成阻塞状态，那就和GPIO_Captured捕获一样，写成外部调用
    # print(response)
    # os.system('arm-none-eabi-gdb -q -x gdb_script.py MailBox.elf')

def USB_Sample_OS(e):
    e.wait()
    os.system('python3 pyusb_fx2_samples.py')    # 到USB传输数据前需要200毫秒


if __name__ == "__main__":
    
    # file_object = open(str(sys.argv[2]) + '.txt', 'w')
    # Capturedfile_Name = '-' + str(sys.argv[1])
    # Capturedfile_Format = '.vcd' # 这个在这个脚本里目前没使用20190313
    # CapturedGPIO_Name = '-GPIO_Timestamp'
    # CapturedGPIO_Format = '.txt'
    CapturedTimes = 1#sys.argv[3] #GPIO_Interrupt目前在有边沿到来后一次捕获1100个时间戳
    
    gdb.execute('target remote localhost:3333')
    gdb.execute('monitor reset')
    gdb.execute('monitor halt')
    gdb.execute('load')
    # gdb.execute('monitor resume')   
    
    e = multiprocessing.Event()
    # task_Captured_GPIO = multiprocessing.Process(name = 'block', target = Captured_GPIO, args = (e,))
    # task_USB_Sample = multiprocessing.Process(name = 'block', target = USB_Sample, args = (e,))
    # task_GDB_Command = multiprocessing.Process(name = 'block', target = GDB_Command, args = (e,))
    task_USB_Sample_OS = multiprocessing.Process(name = 'block', target = USB_Sample_OS, args = (e,))    # 在这个进程里用subprocess.Popen方法非阻塞外部调用GPIO_Interrupt程序捕捉定期触发的GPIO
    
    # gdb.execute('target remote localhost:3333')
    # gdb.execute('monitor reset')
    # gdb.execute('monitor halt')
    # gdb.execute('load')
    # gdb.execute('monitor resume')

    # time.sleep(5)

    # task_USB_Sample.start()
    
    task_USB_Sample_OS.start()
    # task_Captured_GPIO.start()
    
    # time.sleep(5)
    
    e.set()
    time.sleep(0.415)    # 等到pyusb_fx2_samples.py跑到采集前的位置
    print('恢复target的运行')
    gdb.execute('monitor resume')  
    
    
    # task_GDB_Command.start()
    # gdb.execute('monitor resume')

    # subprocess.getstatusoutput('arm-none-eabi-gdb -q -x gdb_script.py MailBox.elf')

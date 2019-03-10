import usb.core
import usb.util
import time
import sys
from vcd import VCDWriter
from array import array


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
samples =  4096#4096*128*2 # ,在24MHz下这个数字最小是512，比这个还小就会卡死

# 先读一次，使buf不为空
ret = dev.ctrl_transfer(0x40,0xb1,0,0,Setdata,0x0300)
buf = intf[0].read(samples)
# buf_output = buf.tolist()
# print(buf)
filename = 'mailbox_samples.txt'
file_object = open(filename,'w')

for i in range(0,len(buf)):
    file_object.write(bin(buf[i]).replace('0b',''))
    file_object.write('\n')

file_object.close()


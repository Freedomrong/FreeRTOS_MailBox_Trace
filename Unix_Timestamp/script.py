#!/usr/bin/env python3
# coding=utf-8
import time
import subprocess
import sys
import os
import shutil
import multiprocessing

# 函数定义
'''寻找list与给定数字最接近的数的索引'''
def find_closest(L, target): #L
    L.sort(reverse=False)
    for i in range(0,len(L)):
        if target > L[i] and target < L[i+1]:
            left_abs = abs(target - L[i])
            right_abs = abs(target - L[i+1])
            if right_abs > left_abs:    # 左边距离近
                return i
                break
            if left_abs > right_abs:    # 右边距离近
                return i+1
                break
            if left_abs == right_abs:   # 两边距离相等返回小于它的那个数的索引
                return i
                break


'''STEP1'''
input_file = '0-Mail_Box_Tracing.vcd'
output_txt_file = '0data-Mail_Box_Tracing.txt'

vcd2txt_command = ('sigrok-cli -I vcd -i ' + input_file + ' >> ' + output_txt_file)

response = subprocess.getstatusoutput(vcd2txt_command)

input_file = '0-Mail_Box_Tracing.vcd'
output_txt_decode_file = '0decode-data-Mail_Box_Tracing.txt'
decode_command = ('sigrok-cli -I vcd -i ' + input_file + ' -P uart:rx=SWO:baudrate=8000000,arm_tpiu:stream=1,arm_itm' + ' >> ' + output_txt_decode_file)
response = subprocess.getstatusoutput(decode_command)


output_txt_itm_file = '0-itm-decode-data-Mail_Box_Tracing.txt'
response = subprocess.getstatusoutput("grep -rn 'itm' " + output_txt_decode_file + " >> " + output_txt_itm_file)


'''STEP2'''
outputTick_txt_file = ('Tick-' + output_txt_file)
grepTick_command = ("grep -rn 'Tick'" + output_txt_file + ' >> ' + outputTick_txt_file)    # 在windows中安装了'GREP for windows' -- http://www.interlog.com/~tcharron/grep.html
# response = subprocess.getstatusoutput(grepTick_command)
subprocess.getstatusoutput("grep -rn 'Tick' 0data-Mail_Box_Tracing.txt >> Tick-0data-Mail_Box_Tracing.txt")

file_object = open(outputTick_txt_file, 'r')
try:
    data_lines = file_object.readlines()
finally:
    file_object.close()

data_spilt1_lines = []

for i in range(0,len(data_lines)):
    temp1 = data_lines[i].split(':')    # 按':'切割
    data_spilt1_lines.append(temp1[2])  # temp[0]是行号，temp[1]是'LE2_Tick'

# print(data_spilt1_lines)

data_spilt2_lines = []

for i in range(0,len(data_spilt1_lines)):
    # temp2 = data_spilt1_lines[i].split('\n')    # 按'\'切割
    temp2 = data_spilt1_lines[i].strip('\n')    # 删除'\n'
    data_spilt2_lines.append(temp2)

data_spilt3_lines = []

for i in range(0,len(data_spilt2_lines)):
    temp3 = data_spilt2_lines[i].split(' ')    # 按' '切割
    data_spilt3_lines.append(temp3)

data_divided = []

for n in range(0,len(data_spilt3_lines)):    # 最外层
    for i in range(0,len(data_spilt3_lines[n])):    # 内1层是list，list的元素是字符串
        for k in range(0,len(data_spilt3_lines[n][i])):    # 内2层是字符串，字符串的元素是字符
            data_divided.append(data_spilt3_lines[n][i][k])
            # print(data_spilt3_lines[n][i][k])             # data_spilt3_lines[0]有64个字符

for i in range(0,len(data_divided)):
    if data_divided[i] == '1':
        if data_divided[i + 1] == '1':
            if data_divided[i + 1 + 1] == '1':
                # print(i)
                zero2one_gap = i    # 1个间隔是1ns
                break

print('从开始到第1个Tick上升沿所经历的时间为:%fs' % ((zero2one_gap * 1)/1000000000))

'''STEP3'''
Mark_file = 'Mark.txt'

file_object = open(Mark_file, 'r')
try:
    data_lines = file_object.readlines()
finally:
    file_object.close()

Mark_spilt1_lines = []

for i in range(0,len(data_lines)):
    temp1 = data_lines[i].split('--')    # 按'--'切割，还需要删除\\')\n
    Mark_spilt1_lines.append(temp1[1])  #

Mark_spilt2_lines = []

for i in range(0,len(Mark_spilt1_lines)):
    temp2 = Mark_spilt1_lines[i].strip("\\')\n")    # 20181230 删除\\')\n
    Mark_spilt2_lines.append(temp2)

Mark_timestamp = []

for i in range(0,len(Mark_spilt2_lines)):
    temp3 = float(Mark_spilt2_lines[i])
    Mark_timestamp.append(temp3)

'''STEP4'''
GPIOtimestamp_file = '0-GPIO_Timestamp.txt'

file_object = open(GPIOtimestamp_file, 'r')
try:
    data_lines = file_object.readlines()
finally:
    file_object.close()

GPIO_spilt1_lines = []

for i in range(0,len(data_lines)):
    temp1 = data_lines[i].split('--')    # 按'--'切割，还需要删除\n
    GPIO_spilt1_lines.append(temp1[1])  #

GPIO_timestamp = []

for i in range(0,len(GPIO_spilt1_lines)):
    temp2 = GPIO_spilt1_lines[i].strip('\n')    # 20181231 删除\n
    GPIO_timestamp.append(float(temp2))

WP0GPIOtimestamp_first = GPIO_timestamp[find_closest(GPIO_timestamp, Mark_timestamp[0] + (zero2one_gap * 1)/1000000000)]
print("在GPIO捕获的Tick时间中与预估时间最为接近的时间：%fs" %WP0GPIOtimestamp_first)


'''数出0-itm-decode-data-Mail_Box_Tracing.txt文件中抓GPIO的Watchpoint0的个数'''
'''然后从WP0GPIOtimestamp_first开始作为第一个Watchpoint0的时间，依次给这些Watchpoint0赋GPIO_timestamp'''   # add by 20181231

print('###')




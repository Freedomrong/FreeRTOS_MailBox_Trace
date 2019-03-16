#!/usr/bin/env python
# coding=utf-8
import gdb

print('启动了gdb脚本')

gdb.execute('target remote localhost:3333')
gdb.execute('monitor reset')
gdb.execute('monitor halt')
gdb.execute('load')
# gdb.execute('continue')
gdb.execute('monitor resume')

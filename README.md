## FreeRTOS 邮箱队列追踪

### 1. 使用STM32CubeMX生成两个进程  
   Creating two FreeRTOS tasks by using STM32CubeMX

### 2. 两个进程间通过使用cmsis_os.h中的Mail函数实现基于Mailbox的进程间同步  
   Based on Mail function of cmsis_os.h

### 3. 开启硬件辅助追踪  
   Opening hardware assisted tracing


### 4. 修改sigrok-cli的源代码
   We edit the code in session.c of sigrokcli-0.5.0<br>
   `From`
   ```c
   if (sr_session_start() != SR_OK) {
      g_critical("Failed to start session.");
      sr_session_destroy();
      return;
   }
   ```
   `To`
   ```c
   if (sr_session_start() != SR_OK) {
      g_critical("Failed to start session.");
      sr_session_destroy();
      return;
   }else
   {
      printf("Begin");
      Print_Timestamp();
   }
   ```
   `And the definition of Print_Timestamp`
   ```c
   int Print_Timestamp()
   {
      /*Unix年月日十分秒*/
      time_t t;
      struct tm * lt;
      time(&t);
      lt = localtime(&t);
      struct timeval tv;

      gettimeofday(&tv, NULL);
      // 注意在C语言函数库中，月份是0到11,0是实际的1月，11是12月份是
      printf("c timestamp: %d/%d/%d %d:%d:%d --%ld.%06ld\n",lt->tm_year+1900, lt->tm_mon+1, lt->tm_mday, lt->tm_hour, lt->tm_min, lt->tm_sec, tv.tv_sec,tv.tv_usec)
   }
   ```

### 5. 目前上传PyUSB还是早期版本
    pyusb_fx2_samples.py is a sample script which saving as txt format and using in raspberry pi.(python3 fx2_samples.py)
    pyusb_sample_fx2_vcd.py is a txt format to vcd for sigrok script which using in PC.(python3 pyusb_sample_fx2_vcd.py mailbox_samples.txt >> mailbox_samples.vcd)
    script.py is a automatic script for USB sample Tracing data and GPIO captured.

    gcc -lwiringPi Datetime_GPIO_Interrupt.c -o Datetime_GPIO_Interrupt

    Please remeber add timescale 41666667 in TIMESCALE_NUMS of writer.py(/usr/local/lib/python3.4/dist-packages/vcd)
    
### 6. 关于时间同步的说明
    不要被sigrok和pulseview的timestamp数据误导,ITM发出的增量时间戳包只是两次发出时间戳包之间的间隔机器时间,21位的计数器就是负责记这个间隔时间的,重发包则计数器清0重新记,所以设计同步方案和计数器是否清0无关.
    unix时间戳有两个目的，1. 让增量时间戳和标准世界时间能够对应 2. 强行同步追踪数据和真实事件.
    对于1，不需要（也不可能）给每个增量时间戳都找到对应的unix时间戳
    对于2，追踪数据中的Watchpoint是一个桥梁，能记录下GPIO翻转，并能把这个记录输出到追踪数据中.
    所以对GPIO翻转记录时间戳 = 给追踪数据中的Watchpoint记录时间戳 = 给追踪数据中距离Watchpoint最近的增量时间戳找到对应的标准世界时间.


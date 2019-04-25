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
    **pyusb_fx2_samples.py** is a sample script which saving as txt format and using in raspberry pi.
    **pyusb_sample_fx2_vcd.py** is a txt format to vcd for sigrok script which using in PC.
    **script.py** is a automatic script for USB sample Tracing data and GPIO captured.

    gcc -lwiringPi Datetime_GPIO_Interrupt.c -o Datetime_GPIO_Interrupt


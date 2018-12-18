#### (1)由于DWT_Watchpoint（仍然通过ITM输出）可以捕获我们插桩在Tick中的GPIO翻转的，而且Tick实际是一个定时器中断函数，以1ms为周期，ITM能够记录下来CPU进入中断状态，所以我们在时间刻度上，让GPIO翻转与DWT_Watchpoint捕获的Tick中的GPIO的信息对齐;
#### (2)再加上我们使用RaspberryPi也捕获这个GPIO翻转就能将程序内部时间与外界成功关联起来，所以我们将时间戳打在RaspberryPi的捕获GPIO上（上升沿与下降沿）
#### (3)sigrok的捕获与GPIO捕获应该同时开启,标志sigrok开始捕获的时间戳仍然应该被获得，并选择与之最近的GPIO捕获时间戳进行对齐，否则仍然不知道捕获出来的数据时间是多少
#### (4)不专门设计多进程同步执行的话，应该是先开启GPIO捕获，再开GPIO捕获

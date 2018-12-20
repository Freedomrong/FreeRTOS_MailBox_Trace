'''
写出两个进程，一个进程运行到另一个进程结束后它才结束
'''

import multiprocessing
import time
def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print ('wait_for_event: starting')
    e.wait()
    print("恢复wait_for_event")
    print ('wait_for_event: e.is_set()->' + str(e.is_set()))

def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print ('wait_for_event_timeout: starting')
    e.wait(t)
    print("恢复wait_for_event_timeout")
    print ('wait_for_event_timeout: e.is_set()->' + str(e.is_set()))


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block', 
                                 target=wait_for_event,
                                 args=(e,))
    w1.start()

    w2 = multiprocessing.Process(name='non-block', 
                                 target=wait_for_event_timeout, 
                                 args=(e, 2))
    w2.start()

    time.sleep(3)
    e.set()
    print ('main: event is set')

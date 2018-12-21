import multiprocessing
import time


def CapturedGPIO(e):
    """e.wait() will wait until a e.set() in a another place has runned"""
    print ('G1')
    e.wait()
    time.sleep(1)
    print("G2")
    time.sleep(1)
    print("G3")
    time.sleep(1)
    #print ('wait_for_event: e.is_set()->' + str(e.is_set()))

def CapturedCommand(e, t):
    """e.wait(t) will wait t second and then run the after"""
    e.wait(t)

    print ('C1')
    time.sleep(1)
    print("C2")
    time.sleep(1)
    print("C3")
    time.sleep(1)
    
    """e.set() will resume all the e.wait()"""
    e.set()

    # print ('wait_for_event_timeout: e.is_set()->' + str(e.is_set()))


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name='block', 
                                 target=CapturedGPIO,
                                 args=(e,))

    w2 = multiprocessing.Process(name='non-block', 
                                 target=CapturedCommand, 
                                 args=(e, 1))
    
    w1.start()
    w2.start()

    # time.sleep(3)
    # e.set()
    # print ('main: event is set')

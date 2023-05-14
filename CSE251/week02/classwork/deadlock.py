import threading
import time


def transfer(lock1: threading.Lock, lock2: threading.Lock):
    
    print(f'{threading.current_thread().name}: acquiring lock 1\n', end="")
    lock1.acquire()
    
    print(f'{threading.current_thread().name}: release lock 1\n', end="")
    lock1.release()
    
    print(f'{threading.current_thread().name}: acquiring lock 2\n', end="")
    lock2.acquire()
    
    print(f'{threading.current_thread().name}: release lock 2\n', end="")
    lock2.release()

def transfer_do(lock1, lock2):
    while True:
        transfer(lock1, lock2)
        transfer(lock2, lock1)

def main():
    
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    
    t1 = threading.Thread(target=transfer_do, args=(lock1, lock2))
    t1.start()
    
    t2 = threading.Thread(target=transfer_do, args=(lock1, lock2))
    t2.start()



if __name__ == '__main__':
    main()
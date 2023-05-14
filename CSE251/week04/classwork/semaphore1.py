import queue
import threading
import time

def display(i, sem: threading.Semaphore):
    
    print(f'{threading.current_thread().name}: value before acquire = {sem._value}\n', end="")
    sem.acquire()
    print(f'{threading.current_thread().name}: CRITICAL_CODE, value after acquire = {sem._value}\n', end="")

def increment(sem: threading.Semaphore):
    time.sleep(4)
    sem.release()

def main():
    sem = threading.Semaphore(3)
    
    threads = []
    for i in range(4):
        t = threading.Thread(target=display, args=(i, sem))
        t.start()
        threads.append(t)
    
    t = threading.Thread(target=increment, args=(sem,))
    t.start()
    
    for t in threads:
        t.join()
    t.join()


if __name__ == '__main__':
    main()
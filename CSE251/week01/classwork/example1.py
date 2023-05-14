import threading
import time

class MyThread(threading.Thread):
    def __init__(self, message):
        threading.Thread.__init__(self)
        self.message = message
        self.result = {}

    def run(self):
        time.sleep(0.75)
        print(f'{self.message=}')
        self.result = {"key": 1}

def dummy(message):
    time.sleep(0.5)
    print(f'{message=}')

def main():
    my_thread = MyThread("hello")
    my_thread.start()
    my_thread.join()
    print(f'{my_thread.result=}')
    
    #t1 = threading.Thread(target=dummy, args=("asdfjadskfa",))
    #t1.start()
    
    #print('next line')

main()
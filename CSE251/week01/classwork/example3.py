import threading

count_global = 0


class MyThread(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number

    def run(self):
        global count_global
        count_global = self.number + count_global


def main():

    threading = []
    for _ in range(100):
        t1 = MyThread(1)
        t1.start()
        threading.append(t1)
        
    for t in threading:
        t.join()
    
    print(f'{count_global=}')


if __name__ == '__main__':
    main()

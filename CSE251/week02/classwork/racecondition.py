import threading
import time 
import random

global_counter = 0

def increase(number: int):
    global global_counter
    
    local_counter = global_counter
    
    local_counter += number
    
    time.sleep(random.uniform(0.1, 1))

    global_counter = local_counter
    print(f'{threading.current_thread().name}: {local_counter=}')
    print(f'{threading.current_thread().name}: {global_counter=}')


def main():
    
    t1 = threading.Thread(target=increase, args=(10,))
    t1.start()
    #t1.join()
    #print(f'{global_counter=}')
    
    t2 = threading.Thread(target=increase, args=(20,))
    t2.start() 

    t1.join()
    t2.join()
    print(f'AFTER: {global_counter=}')

if __name__ == '__main__':
    main()
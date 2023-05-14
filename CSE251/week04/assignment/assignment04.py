'''
Questions:
1. Do you need to use locks around accessing the queue object when using multiple threads? 
   Why or why not?
   >Yes
   >When multiple threads are accessing the same queue object, there is a possibility
   that two or more threads could try to access or modify the same data at the same
   time, leading to unexpected or incorrect behavior.

2. How would you define a semaphore in your own words?
   > In my own understanding, semaphore are like if/else statement. Instead of if statement we use a
   semaphore.
   >A semaphore consists of a counter and a queue of waiting threads.

3. Read https://stackoverflow.com/questions/2407589/what-does-the-term-blocking-mean-in-programming.
   What does it mean that the "join" function is a blocking function? Why do we want to block?
   >the join() method is used to wait for a thread to complete its execution before moving on to the next
   >step in the program. The join() method is a blocking function because it blocks the main thread of
   execution until the thread being joined completes its work.
   >Blocking can be useful in situations where you need to ensure that a particular thread or set of
   threads have completed their work before continuing with the next step in the program.
'''

from datetime import datetime
import time
import threading
import random
# DO NOT import queue

from plots import Plots

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

#########################
# NO GLOBAL VARIABLES!
#########################


class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru',
                 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus',
                 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE', 'Super', 'Tall', 'Flat', 'Middle', 'Round',
                  'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                  'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has just be created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, car_count, cars_left, queue, sem_track):

        # this part of the code initializes a class with instance variables and synchronization 
        # objects for multi-threading, and it inherits properties and methods from its parent 
        # class using the super().__init__() call. Every varaiable and object is initialized
        super().__init__()
        self.car_count = car_count
        self.queue = queue
        self.cars_left = cars_left
        self.sem_track = sem_track





    def run(self):
        for i in range(self.car_count):

            #This code creates an instance of a Car class and releases a lock on a shared resource called "cars_left".
            #It then acquires a lock on a shared resource called "sem_track", puts the Car instance into a queue, and
            #repeats the process until the queue is full. it puts None into the queue, releases the lock on "cars_left",
            #and exits the loop.

            car = Car()
            self.cars_left.release()
            self.sem_track.acquire()
            self.queue.put(car)
        self.queue.put(None)
        self.cars_left.release()


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self, queue, cars_left, sem_track, queue_stats):

        #This code is initializing a class with a queue, a semaphore object for synchronization
        #between threads, and a lock object from the threading module. The
        #super().__init__() call initializes the parent class and allows the current class to inherit
        #its properties and methods.

        super().__init__()
        self.queue = queue
        self.cars_left = cars_left
        self.sem_track = sem_track
        self.queue_stats = queue_stats





    def run(self):
        while True:

            #This code acquires a lock on a shared resource called "cars_left" and releases a lock on a
            #shared resource called "sem_track". It then retrieves an object from a queue and checks if
            #it is None. If it is not None, it updates a statistic based on the current size of the queue.
            #If it is None, it breaks out of the loop.

            self.cars_left.acquire()
            self.sem_track.release()
            cars = self.queue.get()

            if cars == None:
                break
            else:
                self.queue_stats[self.queue.size()-1] += 1

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    # Start a timer
    begin_time = time.perf_counter()

    # random amount of cars to produce
    CARS_TO_PRODUCE = random.randint(500, 600)

    #Create Semaphore
    cars_left = threading.Semaphore(0)
    sem_track = threading.Semaphore(MAX_QUEUE_SIZE)

    #Create a queue
    queue = QueueTwoFiftyOne()


    #Create a lock
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership,
    # the index of the list is the size of the queue. Update this list each time the
    # dealership receives a car (i.e., increment the integer at the index using the
    # queue size).
    queue_stats = [0] * MAX_QUEUE_SIZE

    #This code creates an instance of a Manufacturer class with a specified number of
    #cars to produce, and passes in references to shared resources (cars_left, queue,
    #sem_track) that will be used in the manufacturing process.
    manufacturer = Manufacturer(car_count=CARS_TO_PRODUCE, cars_left=cars_left, queue=queue, sem_track=sem_track)

    #This code creates an instance of a Dealership class and passes in references to shared
    #resources (sem_track, queue, cars_left, queue_stats) that will be used to manage the
    #dealership's inventory.
    dealership = Dealership(sem_track=sem_track, queue=queue, cars_left=cars_left, queue_stats=queue_stats)

    #Start dealership and manufacturer
    manufacturer.start()
    dealership.start()


    #Join dealership and manufacturer
    manufacturer.join()
    dealership.join()
    

    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

    # Plot car count vs queue size
    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats,
             title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')


if __name__ == '__main__':
    main()

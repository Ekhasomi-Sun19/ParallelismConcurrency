'''  
Questions:
1. How would you define a barrier in your own words?
   > A barrier is a way to synchronize threads. It is a point in the 
   program where all threads must stop and wait until all threads reach that point. 
   Once all threads reach that point, they can continue executing.
   
2. Why is a barrier necessary in this assignment?
   > A barrier is necessary in this assignment because we need to make sure that all manufacturers 
    have finished producing cars before the dealerships start buying them. If we don't have a barrier,
    then the dealerships might start buying cars before all the manufacturers have finished producing
    cars. This would cause the number of cars produced by the manufacturers to not equal the number of
    cars bought by the dealerships. 
   >
'''

from datetime import datetime, timedelta
import time
import threading
import random

# Global Constants
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!


class Car():
    """ This is the Car class that will be created by the manufacturers """

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

        # Display the car that has was just created in the terminal
        self.display()

    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class QueueTwoFiftyOne():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Manufacturer(threading.Thread):
    """ This is a manufacturer.  It will create cars and place them on the car queue """

    def __init__(self, cars_left, queue, sem_track, manufacturer_stats, manufacturer_id, barrier, dealer_count):

        # this part of the code initializes a class with instance variables and synchronization
        # objects for multi-threading, and it inherits properties and methods from its parent
        # class using the super().__init__() call. Every varaiable and object is initialized
        super().__init__()
        self.cars_to_produce = random.randint(200, 300)
        self.queue = queue
        self.dealer_count = dealer_count
        self.manufacturer_id = manufacturer_id
        self.cars_left = cars_left
        self.sem_track = sem_track
        self.manufacturer_stats = manufacturer_stats
        self.barrier = barrier





    def run(self):
        for i in range(self.cars_to_produce):

            #This code creates an instance of a Car class and releases a lock on a shared resource called "cars_left".
            #It then acquires a lock on a shared resource called "sem_track", puts the Car instance into a queue, and
            #repeats the process until the queue is full. it puts None into the queue, releases the lock on "cars_left",
            #and exits the loop.

            car = Car()
            self.cars_left.release()
            self.sem_track.acquire()
            self.queue.put(car)
            self.manufacturer_stats[self.manufacturer_id] += 1
        self.barrier.wait()

        if self.manufacturer_id == 0:
            for i in range(self.dealer_count):
                self.queue.put(None)
                self.cars_left.release()
                self.sem_track.acquire()


class Dealership(threading.Thread):
    """ This is a dealership that receives cars """

    def __init__(self, queue, cars_left, sem_track, dealer_stats, dealer_id):

        #This code is initializing a class with a queue, a semaphore object for synchronization
        #between threads, and a lock object from the threading module. The
        #super().__init__() call initializes the parent class and allows the current class to inherit
        #its properties and methods.

        super().__init__()
        self.queue = queue
        self.cars_left = cars_left
        self.dealer_id = dealer_id
        self.sem_track = sem_track
        self.dealer_stats = dealer_stats



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
                self.dealer_stats[self.dealer_id] += 1

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def run_production(manufacturer_count, dealer_count):
    """ This function will do a production run with the number of
        manufacturers and dealerships passed in as arguments.
    """

    #Start a timer
    begin_time = time.perf_counter()

    #Create semaphore(s)
    cars_left = threading.Semaphore(0)
    sem_track = threading.Semaphore(MAX_QUEUE_SIZE)

    #Create queue
    car_queue = QueueTwoFiftyOne()


    #Create lock(s)
    lock = threading.Lock()


    #Create barrier(s)
    #In the code above, it represents the number of threads 
    #that need to wait at the barrier before they can proceed. 
    barrier = threading.Barrier(manufacturer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    manufacturer_stats = list([0] * manufacturer_count)

    #create your manufacturers, each manufacturer will create CARS_TO_CREATE_PER_MANUFACTURER
    manufacturers = []
    for manufacturer in range(manufacturer_count):
        manufacturer = Manufacturer(manufacturer_id=manufacturer, manufacturer_stats=manufacturer_stats, cars_left=cars_left, dealer_count=dealer_count, queue=car_queue, sem_track=sem_track, barrier=barrier)
        manufacturers.append(manufacturer)


    #create your dealerships
    dealerships = []
    for dealership in range(dealer_count):
        dealership = Dealership(dealer_id=dealership, sem_track=sem_track, queue=car_queue, cars_left=cars_left, dealer_stats=dealer_stats)
        dealership.start()
        dealerships.append(dealership)


    #Start all manufacturers
    for manufacturer in manufacturers:
        manufacturer.start()

    #Wait for manufacturers and dealerships to complete
    for manufacturer in manufacturers:
        manufacturer.join()


    for dealership in dealerships:
        dealership.join()

    run_time = time.perf_counter() - begin_time

    # This function must return the following - only change the variable names, if necessary.
    # manufacturer_stats: is a list of the number of cars produced by each manufacturer,
    #                collect this information after the manufacturers are finished.
    return (run_time, car_queue.get_max_size(), dealer_stats, manufacturer_stats)
 

def main():
    """ Main function """

    # Use 1, 1 to get your code working like the previous assignment, then
    # try adding in different run amounts. You should be able to run the
    # full 7 run amounts.
    #runs = [(1, 1)]
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for manufacturers, dealerships in runs:
        run_time, max_queue_size, dealer_stats, manufacturer_stats = run_production(
            manufacturers, dealerships)

        print(f'Manufacturers       : {manufacturers}')
        print(f'Dealerships         : {dealerships}')
        print(f'Run Time            : {run_time:.2f} sec')
        print(f'Max queue size      : {max_queue_size}')
        print(f'Manufacturer Stats  : {manufacturer_stats}')
        print(f'Dealer Stats        : {dealer_stats}')
        print('')

        # The number of cars produces needs to match the cars sold (this should pass)
        assert sum(dealer_stats) == sum(manufacturer_stats)


if __name__ == '__main__':
    main()

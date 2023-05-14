from datetime import datetime, timedelta
import math
import threading
import time

# Global count of the number of primes found and numbers examined
prime_count = 0

# Global count of the numbers examined
numbers_processed = 0

NUMBER_THREADS = 10

#This function defines a function called is_prime, which takes an integer 
#as input and returns a boolean value indicating whether or not the input 
# integer is prime.

def is_prime(n: int):
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

#Created a function that takes in two integer arguments, start and end 
#to find the primes in a range It uses a for loop to iterate through each 
# number in the range, and calls the is_prime function to determine whether 
# each number is prime or not. 

def find_primes(start: int, end: int):
    global prime_count, numbers_processed

    # Count the number of primes in this range
    count = 0
    for i in range(start, end + 1):
        if is_prime(i):
            count += 1

    # Update global counts
    prime_count += count
    numbers_processed += (end - start + 1)

if __name__ == '__main__':
    # Start a timer
    begin_time = time.perf_counter()

    # Define the range of numbers to examine for primes
    start_number = 10_000_000_000
    range_size = 110_003


    end_number = start_number + range_size - 1

    # Determine the number of numbers each thread should examine
    num_numbers_per_thread = math.ceil(range_size / NUMBER_THREADS)

    # Create the threads
    threads = []
    for i in range(NUMBER_THREADS):
        # Determine the start and end numbers for this thread
        start = start_number + i * num_numbers_per_thread
        end = min(start_number + (i + 1) * num_numbers_per_thread - 1, end_number)

        # Create the thread and add it to the list
        t = threading.Thread(target=find_primes, args=(start, end))
        threads.append(t)

    # Start the threads
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
   
    # Use the below code to check and print your results
    assert numbers_processed == 110_003, f"Should check exactly 110,003 numbers but checked {numbers_processed}"
    assert prime_count == 4764, f"Should find exactly 4764 primes but found {prime_count}"

    print(f'Numbers processed = {numbers_processed}')
    print(f'Primes found = {prime_count}')
    total_time = "{:.2f}".format(time.perf_counter() - begin_time)
    print(f'Total time = {total_time} sec')

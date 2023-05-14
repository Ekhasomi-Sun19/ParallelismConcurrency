'''
Requirements:
1. Write a function that takes a number and computes the sum of all numbers between
   one and that number (exclusive). This will be the target of your thread.
2. Create a thread to run this function.
3. Assert that your sums are correct for the given number.
   
Psuedocode:
1. Create either a global SUM or create a list object in main.
2a. If using a global, then inside of your function, set the global equal to the sum.
2b. If using a list object, set the appropriate index position equal to the sum.
3. In main, create a thread to call the sum function using 10.
4. Using assert, check the expected result (see main)
5. Repeat steps 3 and 4, but use 13.
6. Repeat steps 3 and 4, but use 17.

Things to consider:
a. If using a global, what is the correct syntax for creating a thread with one argument?
   (see https://stackoverflow.com/questions/3221655/python-threading-string-arguments)
b. How do you start a thread? (see this week's reading) 
c. How will you wait until the thread is done? (see this week's reading)
d. Do threads (including the main thread) share global variables? (see https://superfastpython.com/thread-share-variables/)
e. If you use a global, how will you ensure that one thread doesn't change the value of
   your global while another thread is using it too? (We haven't learned about locks yet, so you
   won't be able to run your threads simultaneously)
f. How do you modify the value of a global variable (see https://stackoverflow.com/questions/10588317/python-function-global-variables)
g. If using a list object, how to you instantiate it with the correct number of indexes? (see https://stackoverflow.com/questions/8528178/list-of-zeros-in-python)
'''
import threading

def sum_numbers(number):
    global SUM
    SUM = 0
    for i in range(1, number):
        SUM += i
    return SUM

#Create a thread to run this function.
def main():
    results = [0] * 3
    numbers = [10, 13, 17]
    threads = list()
    for index, number in enumerate(numbers):
        print(f"Main    : create and start thread {index}.")
        x = threading.Thread(target=sum_numbers, args=(number,))
        threads.append(x)
        x.start()

       #Using assert, check the expected result (see main)
    for index, thread in enumerate(threads):
        print(f"Main    : before joining thread {index}.")
        thread.join()
        print(f"Main    : thread {index} done")
        results[index] = sum_numbers(numbers[index])
        assert results[index] == sum_numbers(numbers[index]), f'The sum should equal {sum_numbers(numbers[index])} but instead was {results[index]}'


#In main, create a thread to call the sum function using 10.
#Repeat steps 3 and 4, but use 13.
#Repeat steps 3 and 4, but use 17.
if __name__ == "__main__":
    main()
    print("DONE")
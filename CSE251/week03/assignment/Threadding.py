from datetime import datetime, timedelta
import time
import requests
import json
import threading


# Const Values
TOP_API_URL = 'https://swapi.dev/api'

# http://127.0.0.1:8790

# Global Variables
call_count = 0

#In this code we define a class called ThreadClass that inherit from threading.Thread
# and override the __init__ and run methods. The __init__ method is called when an object 
#object of this class is created
#the url attribute is initialized with the url passed to the constructor of the class 
#and the data attribute is initialized with None The data attribute will later be used to store
#the data retrieved from the server in a separate thread.
 
class ThreadClass(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.data = None

# the run method is called when the start method is called on the object of this class 
# and it calls the requests.get method to get the data from the url and store it in the 
# data attribute this function is use to retrieve data from the server at the specied url
# and store it in the data attribute of the object of this class. The try block contains 
# the code that retrieves the data from the server. The except block is executed if an 
# exception is raised during the execution of the try block

    def run(self):
        try:
            response = requests.get(self.url)
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from {self.url}: {e}")

def print_film_details(film, chars, planets, starships, vehicles, species):
    '''
    Print out the film details in a formatted way
    '''
    
    def display_names(title, name_list):
        print('')
        print(f'{title}: {len(name_list)}')
        names = sorted([item["name"] for item in name_list])
        print(str(names)[1:-1].replace("'", ""))

    print('-' * 40)
    print(f'Title   : {film["title"]}')
    print(f'Director: {film["director"]}')
    print(f'Producer: {film["producer"]}')
    print(f'Released: {film["release_date"]}')

    display_names('Characters', chars)
    display_names('Planets', planets)
    display_names('Starships', starships)
    display_names('Vehicles', vehicles)
    display_names('Species', species)


def main():

     #Start a timer
    begin_time = time.perf_counter()
    
    print('Starting to retrieve data from the server')

    # This code is retrieving data from an API and populating a dictionary categories 
    # with the results of each API call. It first initializes an empty dictionary categories 
    # and sets call_count to 0. Then, it sends a request to the API using requests.get and 
    # extracts the response as a JSON object using the .json() method. It iterates over each 
    # category in the JSON object, gets the URL for that category, and creates a new ThreadClass 
    # object with that URL. It starts the thread, waits for it to complete using thread.join(), 
    # and then adds the result (stored in thread.data) to the categories dictionary with the category 
    # name as the key.
    categories = {}
    call_count = 0
    try:
        Data_Retrieve_API = requests.get(TOP_API_URL).json()
        for category in Data_Retrieve_API.get('categories', []):
            url = category.get('url')
            if url is not None:
                thread = ThreadClass(url)
            thread.start()
            thread.join()
            if thread.data is not None:
                categories[category['name']] = thread.data
            call_count += 1
    except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from {TOP_API_URL}: {e}")
            return

    print(f"Retrieved {call_count} urls from the server")
    print(categories)

    
    # The part of the program will retrieve the details film with an IDE of 6 by calling the 
    # print_film_details function. The function takes a film id as a parameter and returns the
    # in the film_details. The code then checks if film_details is not None, indicating that 
    # the function call was successful and returned some data. If film_details is not None, the 
    # code assigns None to several variables, including release_date, other_details, planets, 
    # starships, vehicles, and species. The * operator is used to assign any extra values in 
    # film_details to the other_details variable.

    film_id = 6
    film_details = print_film_details(film_id)
    if film_details is not None:
        release_date, *other_details = film_details = planets = starships = vehicles = species = None
        if len(other_details) >= 4:
             planets, starships, vehicles, species = other_details
        print_film_details(film_id, release_date, planets, starships, vehicles, species)

    
    # Iterate over each of the keys in the sixth film details and get the data
    # for each of the categories (might want to create function to do this)


    print(f'There were {call_count} calls to the server')
    total_time = time.perf_counter() - begin_time
    total_time_str = "{:.2f}".format(total_time)
    print(f'Total time = {total_time_str} sec')
    
    # If you do have a slow computer, then put a comment in your code about why you are changing
    # the total_time limit. Note: 90+ seconds means that you are not doing multithreading
    assert total_time < 15, "Unless you have a super slow computer, it should not take more than 15 seconds to get all the data."
    
    assert call_count == 94, "It should take exactly 94 threads to get all the data"
    

if __name__ == "__main__":
    main()

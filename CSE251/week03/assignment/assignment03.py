from datetime import datetime, timedelta
import time
import requests
import json
import threading

# from cse251s23 import *

# Const Values
TOP_API_URL = 'https://swapi.dev/api/'

# Global Variables
call_count = 0


    # In this code we define a class called ThreadClass that inherit from threading.Thread
    # and override the __init__ and run methods. The __init__ method is called when an object 
    # object of this class is created
    # the url attribute is initialized with the url passed to the constructor of the class
    # and the data attribute is initialized with None The data attribute will later be used to store
    # the data retrieved from the server in a separate thread.

class ThreadClass(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    # the run method is called when the start method is called on the object of this class
    # and it calls the requests.get method to get the data from the url and store it in the
    # data attribute this function is use to retrieve data from the server at the specied url
    # and store it in the data attribute of the object of this class. The try block contains
    # the code that retrieves the data from the server. The except block is executed if an
    # exception is raised during the execution of the try block

    def run(self):
        response = requests.get(self.url)
        global call_count
        if response.status_code == 200:
            self.response = response.json()
            call_count += 1
        else:
            print('RESPONSE = ', response.status_code)

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
    # Start a timer
    begin_time = time.perf_counter()

    print('Starting to retrieve data from the server')

    #For this we are using a custom ThreadClass to make an HTTP request to an
    #API endpoint and retrieve data asynchronously. First, a new instance of
    # the ThreadClass is created, passing in a TOP_API_URL argument. The
    # ThreadClass is a user-defined class that inherits from the threading.
    # Thread class, and is presumably implemented to retrieve data from the URL
    # and store it in a response attribute of the ThreadClass instance.


    t1 = ThreadClass(TOP_API_URL)
    t1.start()
    t1.join()
    print(f'{t1.response=}')
    film_1 = t1.response["films"] + '6'

    t2 = ThreadClass(film_1)
    t2.start()
    t2.join()
    print(f'{t2.response=}')

    print(f'{t2.response["characters"]=}')
    print(f'{t2.response["planets"]=}')
    print(f'{t2.response["starships"]=}')
    print(f'{t2.response["vehicles"]=}')
    print(f'{t2.response["species"]=}')

    character_urls = t2.response["characters"]
    planets_urls = t2.response["planets"]
    starships_urls = t2.response["starships"]
    vehicles_urls = t2.response["vehicles"]
    species_urls = t2.response["species"]

    # Iterate over each of the keys in the sixth film details and get the data
    # for each of the categories (might want to create function to do this)


    #This loop iterates through a list called character_urls, which presumably
    #contains URLs to web pages or API endpoints that return data about
    #characters. After creating the ThreadClass instance for a given URL, the
    #start() method is called on the instance, which starts the new thread and
    #begins the process of retrieving data from the URL. This process is repeated
    #for planet, starship, vehicle, and species as shown below.

    threads = []
    for url in character_urls:
        t = ThreadClass(url)
        t.start()
        threads.append(t)

    characters = []
    for t in threads:
        t.join()
        characters.append(t.response["name"])

    print(f'{characters=}')

    threads = []
    for url in planets_urls:
        t = ThreadClass(url)
        t.start()
        threads.append(t)

    planets = []
    for t in threads:
        t.join()
        planets.append(t.response["name"])

    print(f'{planets=}')

    threads = []
    for url in starships_urls:
        t = ThreadClass(url)
        t.start()
        threads.append(t)

    starships = []
    for t in threads:
        t.join()
        starships.append(t.response["name"])

    print(f'{starships=}')

    threads = []
    for url in vehicles_urls:
        t = ThreadClass(url)
        t.start()
        threads.append(t)

    vehicles = []
    for t in threads:
        t.join()
        vehicles.append(t.response["name"])

    print(f'{vehicles=}')

    threads = []
    for url in species_urls:
        t = ThreadClass(url)
        t.start()
        threads.append(t)

    species = []
    for t in threads:
        t.join()
        species.append(t.response["name"])

    print(f'{species=}')

    # The part of the program will retrieve the details film with an IDE of 6 by calling the
    # print_film_details function. The function takes a film id as a parameter and returns the
    # in the film_details. The code then checks if film_details is not None, indicating that
    # the function call was successful and returned some data. If film_details is not None, the
    # code assigns None to several variables, including release_date, other_details, planets,
    # starships, vehicles, and species. The * operator is used to assign any extra values in
    # film_details to the other_details variable.


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
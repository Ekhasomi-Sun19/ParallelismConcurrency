import threading
import requests


TOP_URL = 'https://swapi.dev/api/'


class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)
            

def get_responses(urls):
    threads = []
    for url in urls:
        t = Request_thread(url)
        t.start()
        threads.append(t)
    
    return threads

def main():
    
    t1 = Request_thread(TOP_URL)
    t1.start()
    t1.join()
    #print(f'{t1.response=}')
    film_1 = t1.response["films"] + '1'
    
    t2 = Request_thread(film_1)
    t2.start()
    t2.join()
    #print(f'{t2.response=}')
    
    #print(f'{t2.response["characters"]=}')
    
    character_urls = t2.response["characters"] # list of urls
    
    character_responses = get_responses(character_urls)


if __name__ == '__main__':
    main()
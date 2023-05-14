"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team02-solution.py
Author: Brother Comeau

Purpose: Playing Card API calls
"""

from datetime import datetime, timedelta
import threading
import time
import requests
import json

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


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        req = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        req.start()
        req.join()


    def get_cards(self):
        threads = []
        for _ in range(52):
            req = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/')
            req.start()
            threads.append(req)
        
        cards = []
        for t in threads:
            t.join()
            if t.response != {}:
                cards.append(t.response['cards'][0]['code'])
        
        return cards

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        return self.get_cards()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'u0g16oj0f2f9'

    deck = Deck(deck_id)

    for i in range(5):
        deck.reshuffle()
        cards = deck.get_cards()
        print(f'New deck of cards (count={len(cards)}) {cards}')

    print()

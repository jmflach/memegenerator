import requests
from bs4 import BeautifulSoup
import json
import random

class PhrasesGetter:

    def __init__(self, query, max_len):
        """Construct a PhrasesGetter

        Args:
            query (string): the query for the request
            n (int): the number of phrases desired
            max_len (int): the maximum lenght of the phrases desired
        """
        self.query = query
        self.link = "https://www.pensador.com/" + query + "/"
        self.max_len = max_len

    def _get_phrases_at_page(self, page):
        """Get all phrases at a specific page that are smaller than self.max_len

        Args:
            page (int): the page number

        Returns:
            dict: contains all the phrases retrieved and the number of phrases retrieved
        """
        phrases = []
        esp = requests.get(self.link + str(page))
        soup = BeautifulSoup(esp.text, "html.parser")
        divs = soup.find_all("div", {"class": "thought-card mb-20"})
    
        for div in divs:
            frase = div.find('p', {"class": "frase"}).get_text()  
            author = div.find('span', {"class": "author-name"}).get_text()
            if (len(frase) < self.max_len):
                phrases.append ({"phrase": frase, "author": author})
                    
        return {"phrases": phrases, "n": len(phrases)}


    def _get_phrase_at_page_index(self, page, i):
        """Get the phrase at specific page and specific index"""
        return self._get_phrases_at_page(page)["phrases"][i]


    def _get_phrase_at_index(self, i):
        """Get the phrase at specific index"""
        page_size = 15
        
        page = i // page_size
        i = i % page_size
        
        print(page, i)
        
        return self._get_phrase_at_page_index(page, i)


    def get_phrases(self, n):
        """Get phrases from https://www.pensador.com/"""
        current_n = 0
        page = 0
        phrases = []
        while(current_n < n and page < 10):
            page +=1
            r = self._get_phrases_at_page(page)
            phrases += r["phrases"]
            current_n += r["n"]
        return {"phrases": phrases[0:n], "n": len(phrases[0:n])}


    def get_random_phrase(self):
        """Get a random phrase from https://www.pensador.com/"""
        r = random.randrange(150)
        print(r)
        return self._get_phrase_at_index(r)
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import socks
import socket
import re
from requests import Session
import time 
from random import choice

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

session = Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

class Content:
    def __init__(self, url, name, dob, birthPlace):
        self.url = url.strip()
        self.name = name.strip()
        self.dob = dob.strip() 
        self.birthPlace = birthPlace.strip()

    def printProfile(self):
        print(
            'Found a new profile...\n'\
            f'Url: {self.url}\n'\
            f'Full Name: {self.name}\n'\
            f'Date of Birth: {self.dob}\n'\
            f'Place of Birth: {self.birthPlace}\n'\
        )

def getPage(url):
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    article = bs.find('div', {'id': 'mw-content-text'})
    return article 

def getDetails(url):
    bs = getPage(url)
    time.sleep(2)
    try:
        name = bs.find('td', {'class': 'infobox-data nickname'}).get_text()
        dob = bs.find('span', {'class': 'bday'}).get_text()
        birthPlace = bs.find('td', {'class': 'infobox-data birthplace'}).get_text()
    except AttributeError:
        return None 
    else:
        content = Content(url, name, dob, birthPlace)
        content.printProfile()
        getLinks(bs)

def getLinks(bs):
    links = bs.find_all('a', href=re.compile('^(/wiki/).*'))
    for i in range(len(links)):
        link = choice(links)
        url = link.attrs['href']
        url = 'https://en.wikipedia.org' + url 
        print(url,'\n')
        getDetails(url)

print(getDetails('https://en.wikipedia.org/wiki/Christiano_Ronaldo'))
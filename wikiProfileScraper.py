from urllib.request import urlopen 
from bs4 import BeautifulSoup
import socks
import socket
import re
from requests import Session
import time 

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socket

session = Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

html = session.get('https://en.wikipedia.org/wiki/Lionel_Messi', headers=headers)

class Content:
    def __init__(self, url, name, dob, birthPlace):
        self.url = url 
        self.name = name 
        self.dob = dob 
        self.birthPlace = birthPlace

    def printProfile(self):
        print(
            f'Url: {self.url}\n'\
            f'Full Name: {self.name}\n'\
            f'Date of Birth: {self.dob}\n'\
            f'Place of Birth: {birthPlace}\n'\
        )

def getPage(url):
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    article = bs.find('div', {'id': 'mw-content-text'})
    return article 

def getDetails(bs):
    try:
        name = bs.find('td', {'class': 'infobox-data nickname'}).get_text()
        dob = bs.find('td', {'class': 'infobox-data'}).get_text()
        birthPlace = bs.find('td', {'class': 'infobox-data birthplace'}).get_text()
    except AttributeError:
        return None 
    else:
        return name, dob, birthPlace 

def getLinks(bs):
    links = bs.find_all('a', href=re.compile('^(https://en.wikipedia.org/wiki/).*'))
    return links 

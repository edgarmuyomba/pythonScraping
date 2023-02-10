from urllib.request import urlopen 
from bs4 import BeautifulSoup
import socks
import socket
import re
from requests import Session
import time 
from random import choice
import pymysql

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

#Setting up a connection to mysql database to store the profiles
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='muyomba', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute ('USE wikipediaProfiles')

session = Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

class Content:
    """
        A class used to organise the details about the discovered profiles
    """
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
    """
        A function used to obtain the article section of a wikipedia page
    """
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    article = bs.find('div', {'id': 'mw-content-text'})
    return article 

def getDetails(url):
    """
        A function used to obtain the details from the discovered profiles on wikipedia
    """
    bs = getPage(url)
    time.sleep(2)
    try:
        name = bs.find('td', {'class': 'infobox-data nickname'}).get_text()
        dob = bs.find('span', {'class': 'bday'}).get_text()
        birthPlace = bs.find('td', {'class': 'infobox-data birthplace'}).get_text()
    except AttributeError:
        #if a page is not a profile page (for a person), the function simply returns None
        return None 
    else:
        content = Content(url, name, dob, birthPlace)
        content.printProfile()
        #After printing the details, links to other profiles are discovered on the page
        getLinks(bs)

def getLinks(bs):
    """
        A function to obtain links to other profiles/pages from a wikipedia page
    """
    links = bs.find_all('a', href=re.compile('^(/wiki/).*'))
    for i in range(len(links)):
        #A link to follow is selected at random and its details further obtained
        link = choice(links)
        url = link.attrs['href']
        url = 'https://en.wikipedia.org' + url 
        print(url,'\n')
        getDetails(url)

def store(url, name, dob, birthPlace):
    cur.execute('INSERT INTO Profiles (url, fullname, DOB, birthPlace) VALUES (%s, %s, %s, %s)', (url, name, dob, birthPlace))
    cur.commit()

if __name__ == '__main__':
    try:
        getDetails('https://en.wikipedia.org/wiki/Christiano_Ronaldo')
    finally:
        cur.close()
        conn.close()


import re
from random import choice
import socks
import socket
from urllib.request import urlopen 
from bs4 import BeautifulSoup

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

books = dict()

def getLinks(url):
    global books
    html = urlopen('https://www.pdfdrive.com'+url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        ebook = bs.find('div', {'class': 'ebook-main'})
        title = ebook.find('h1', {'class': 'ebook-title'}).get_text()
        link = 'https://www.pdfdrive.com' + ebook.find('a').attrs['href']
    except AttributeError:
        print('Not a book Page! Moving on...')
    else:
        if len(books) < 150:
            if title not in books:
                books[title] = link
                print(title, '\t', link)
    bookLists = bs.find_all('div', {'class': 'files-new'})
    links = set()
    for bookList in bookLists:
        bookLinks = bookList.find_all('a')
        for link in bookLinks:
            links.add(link)
    getLinks(choice(list(links)).attrs['href'])

getLinks('')
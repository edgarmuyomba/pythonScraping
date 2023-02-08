from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re 

'https://en.wikipedia.org/wiki/Kevin_Bacon'

pages = dict()

def getLinks(url):
    html = urlopen('https://en.wikipedia.org'+url)
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find('div', {'id': 'mw-content-text'}).find_all('a', href=re.compile('^(/wiki/)'))
    for link in links:
        if link.get_text() not in pages:
            pages[link.get_text()] = link.attrs['href']
            print(link.attrs['href'])
            getLinks(link.attrs['href'])

getLinks('/wiki/Kevin_Bacon')
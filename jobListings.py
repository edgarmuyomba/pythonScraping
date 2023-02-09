import socks 
import socket 
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import time
import requests
import re

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

session = requests.Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

class Content:
    def __init__(self, url, title, company, location):
        self.title = title 
        self.company = company 
        self.location = location 
        self.url = url

    def printListing(self):
        print(
            'Found a new listing...\n'
            f'Url: {self.url}\n'\
            f'Title: {self.title}\n'\
            f'Company: {self.company}\n'\
            f'Location: {self.location}\n'
            )

def getPage(url):
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs

def ugandaJob(keyword):
    keyword = keyword.replace(' ', '+')
    url = 'https://www.ugandajob.com/job-vacancies-search-uganda/' + keyword + '?'
    bs = getPage(url)
    time.sleep(2)
    resultPage = bs.find('div', {'class': 'search-results jobsearch-results'})
    results = resultPage.find_all('div', {'class': 'job-description-wrapper'})
    for result in results:
        try:
            url = result.find('a', href=re.compile('^(/job-vacancies-uganda/).*')).attrs['href']
            url = 'https://www.ugandajob.com' + url
            title = result.find('a', href=re.compile('^(/job-vacancies-uganda/).*')).get_text()
            time.sleep(2)
            company = result.find('a', {'class': 'company-name'}).get_text()
            location = result.find('p').get_text()
        except AttributeError:
            print('Something is wrong here! Moving on...')
        else:
            content = Content(url, title, company, location)
            content.printListing()

if __name__ == '__main__':
    ugandaJob('python developer')


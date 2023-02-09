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
        self.title = title.strip()
        self.company = company.strip()
        self.location = location.strip() 
        self.url = url.strip()

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
    resultBlock = bs.find('div', {'class': 'search-results jobsearch-results'})
    results = resultBlock.find_all('div', {'class': 'job-description-wrapper'})
    for result in results:
        try:
            url = result.find('a', href=re.compile('^(/job-vacancies-uganda/).*')).attrs['href']
            url = 'https://www.ugandajob.com' + url
            title = result.find('a', href=re.compile('^(/job-vacancies-uganda/).*')).get_text()
            time.sleep(2)
            company = result.find('a', {'class': 'company-name'}).get_text()
            location = result.find('p').get_text()
        except AttributeError:
            pass
        else:
            content = Content(url, title, company, location)
            content.printListing()

def theUgandanJobLine(keyword):
    keyword = keyword.replace(' ', '+')
    url = 'https://www.theugandanjobline.com/?s=' + keyword 
    bs = getPage(url)
    time.sleep(2)
    resultBlock = bs.find('div', {'id': 'content'})
    results = resultBlock.find_all('div', id=re.compile('^(post-)[0-9].+'))
    for result in results:
        try:
            url = result.find('a', href=re.compile('^(https://www.theugandanjobline.com).*')).attrs['href']
            time.sleep(2)
            details = result.find_all('p')
            title = details[0].get_text()
            company = details[1].get_text()
            location = details[2].get_text()
        except IndexError:
            try:
                details = result.find_all('div', {'style': 'line-height: normal; margin-bottom: .0001pt; margin-bottom: 0in;'})
                title = details[0].get_text()
                company = details[1].get_text()
                location = details[2].get_text()
            except IndexError as e:
                pass
        except AttributeError as e:
            pass
        else:
            content = Content(url, title, company, location)
            content.printListing()     

def everJobs(keyword):
    keyword = keyword.replace(' ', '%20')
    url = 'https://everjobs.ug/?query=' + keyword + '&category'
    bs = getPage(url)
    results = bs.find('table', {'id': 'wpjb-job-list'}).children
    for result in results:
        try:
            url = result.find('a', href=re.compile('^(https://everjobs.ug/job).*')).attrs['href']
            title = result.find('td', {'class': 'wpjb-column-title'}).get_text()
            time.sleep(2)
            company = result.find('small', {'class': 'wpjb-sub'}).get_text()
            location = result.find('td', {'class': 'wpjb-column-location'}).get_text()
        except AttributeError as e:
            print(e)
        else:
            content = Content(url, title, company, location)
            content.printListing()

if __name__ == '__main__':
    everJobs('python developer')


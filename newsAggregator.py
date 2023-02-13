from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re
import socks 
import socket 
from requests import Session 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time 
import threading

# socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
# socket.socket = socks.socksocket 

session = Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(executable_path=r'F:\geckodriver\geckodriver.exe', options=options)

class Article:
    def __init__(self, url, title, summary, image):
        self.url = url.strip() 
        self.title = title.strip() 
        self.summary = summary.strip() 
        self.image = image.strip() 
    
    def __str__(self):
        return '\nFound a new Article...\n'\
                f'Title: {self.title}\n'\
                f'Summary: {self.summary}\n'
            
def getPage(url):
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs 

def scrapeDailyMonitor(url):
    bs = getPage(url)
    time.sleep(2)
    articles = bs.find_all('section', {'class': 'nested-cols headline-teasers-row'})
    for article in articles:
        try:
            link = article.find('a', href=re.compile('^(/uganda/news/national/).*')).attrs['href']
            link = url + link 
            title = article.find('h3', {'class': 'teaser-image-large_title title-medium'}).get_text().strip('PRIME')
            summary = article.find('p', {'class': 'teaser-image-large_paragraph text-block'}).get_text()
            image = article.find('img', src=re.compile('^(/resource/image/).*')).attrs['src']
        except AttributeError:
            pass 
        else:
            article = Article(link, title, summary, image)
            print(article)

def scrapeNewVision(url):
    driver.get(url)
    time.sleep(2)
    try:
        element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'section-title-left')))
    finally:
        page = driver.page_source
        bs = BeautifulSoup(page, 'html.parser')
        time.sleep(2)
        articles = bs.find_all('div', {'class': 'home-ads-section col-sm-12 col-md-6 col-lg-6 col-xl-6 col'})
        for article in articles:
            try:
                link = article.find('a', href=re.compile('^(/category/world/).*')).attrs['href']
                link = url + link 
                title = article.find('h3', {'class': 'latest-news-title mb-2'}).get_text()
                summary = article.find('p', {'class': 'latest-news-desc mt-n4'}).get_text()
                image = article.find('div', {'class': 'ma-0 pa-0 col-md-6 col'}).find('div', {'class': 'v-image__image v-image__image--preload v-image__image--cover'}).attrs['style']
                image = re.search(r'^.*url\((.*")', image).group(1)
            except AttributeError as e:
                print(e)
            else:
                article = Article(link, title, summary, image)
                print(article)   

def scrapeIndependent(url):
    bs = getPage(url)
    time.sleep(2)
    articles = bs.find_all('article', {'class': 'item-list'})
    for article in articles:
        try:
            link = article.find('a', href=re.compile('^(https://www.independent.co.ug/).*')).attrs['href']
            title = article.find('h2', {'class': 'post_box-title'}).get_text()
            summary = article.find('div', {'class': 'entry'}).find('p').get_text()
            image = article.find('img', src=re.compile('^.*(/wp-content/uploads/).*')).attrs['src']
        except AttributeError as e:
            print(e)
        else:
            article = Article(link, title, summary, image)
            print(article)

def scrapeKfm(url):
    bs = getPage(url)
    time.sleep(2)
    articles = bs.find_all('article', {'class': 'jeg_post jeg_pl_md_2 format-standard'})
    for article in articles:
        try:
            link = article.find('a', href=re.compile('^.*(/lifestyle/).*')).attrs['href']
            title = article.find('h3', {'class': 'jeg_post_title'}).get_text()
            summary = article.find('div', {'class': 'jeg_post_excerpt'}).get_text()
            image = article.find('img').attrs['data-src']
        except AttributeError as e:
            print(e)
        else:
            article = Article(link, title, summary, image)
            print(article)

def scrapeKampalaSun(url):
    bs = getPage(url)
    time.sleep(2)
    articles = bs.find_all('li', {'class': 'list-post pclist-layout'})
    for article in articles:
        try:
            link = article.find('a', href=re.compile('^.*(.co.ug/).*')).attrs['href']
            title = article.find('h2', {'class': 'penci-entry-title entry-title grid-title'}).get_text()
            summary = article.find('div', {'class': 'item-content entry-content'}).get_text()
            image = article.find('a', {'class': 'penci-image-holder penci-lazy'}).attrs['data-bgset']
        except AttributeError as e:
            print(e)
        else:
            article = Article(link, title, summary, image)
            print(article)

dailyMonitor = 'https://www.monitor.co.ug/' #National news
newVision = 'https://www.newvision.co.ug/' #World news
independent = 'https://www.independent.co.ug/business-news/' #Business news
kfm = "https://www.kfm.co.ug/category/lifestyle" #Lifestyle news
kampalaSun = "https://www.kampalasun.co.ug/category/sex-relationships/" #Gossip

t1 = threading.Thread(target=scrapeDailyMonitor, args=(dailyMonitor,))
t2 = threading.Thread(target=scrapeNewVision, args=(newVision,))
t3 = threading.Thread(target=scrapeIndependent, args=(independent,))
t4 = threading.Thread(target=scrapeKfm, args=(kfm,))
t5 = threading.Thread(target=scrapeKampalaSun, args=(kampalaSun,))

if __name__ == '__main__':
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
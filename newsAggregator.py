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

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket 

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
    def __init__(self, url, title, summary, image=None):
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
    try:
        element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'section-title-left')))
    finally:
        page = driver.page_source
        bs = BeautifulSoup(page, 'html.parser')
        articles = bs.find_all('div', {'class': 'home-ads-section col-sm-12 col-md-6 col-lg-6 col-xl-6 col'})
        for article in articles:
            try:
                link = article.find('a', href=re.compile('^(/category/world/).*')).attrs['href']
                link = url + link 
                title = article.find('h3', {'class': 'latest-news-title mb-2'}).get_text()
                summary = article.find('p', {'class': 'latest-news-desc mt-n4'}).get_text()
            except AttributeError as e:
                print(e)
            else:
                article = Article(link, title, summary)
                print(article)   

scrapeDailyMonitor('https://www.monitor.co.ug/uganda')
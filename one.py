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

# socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
# socket.socket = socks.socksocket 

session = Session()
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
    'q=0.9,image/webp,*/*;q=0.8'
}

# options = webdriver.FirefoxOptions()
# options.headless = True
# driver = webdriver.Firefox(executable_path=r'F:\geckodriver\geckodriver.exe', options=options)

def getPage(url):
    global session, headers 
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs 

url = "https://www.kampalasun.co.ug/category/sex-relationships/"
bs=getPage(url)
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
        # print(f'{title}\n{summary}\\n\n\n')
        print(image,'\n')

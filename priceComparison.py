import requests 
import socks 
import socket 
from urllib.request import urlopen 
from bs4 import BeautifulSoup

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket

session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
            'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
            'Accept':'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,*/*;q=0.8'}
 

def averagePrice(adict):
    sum = 0
    for i in adict:
        sum += adict[i]
    return sum / 10

def compareFor(item):
    alibaba = 'https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=all&SearchText=' + item 
    amazon = 'https://www.amazon.com/s?k=' + item + '&ref=nb_sb_noss'
    alibabaPrices = getAlibaba(alibaba)
    amazonPrices = getAmazon(amazon)

    print('\nAmazon prices: %.2f'%averagePrice(amazonPrices))
    print('\nAlibaba prices: %.2f'%averagePrice(alibabaPrices))

def getAlibaba(url):
    global session, headers
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    resultPage = bs.find('div', {'id': 'organic-list app-organic-search__list'})
    results = resultPage.find_all('div', {'class': 'list-no-v2-outter'})
    top10 = dict()
    for i in range(10):
        try:
            title = results[i].find('p', {'class': 'elements-title-normal__content large'}).get_text()
            price = results[i].find('span', {'class': 'elements-offer-price-normal__promotion'}).get_text()
        except AttributeError:
            print('Something is wrong here! Moving on...')
        else:
            top10[title] = price 
    return top10

def getAmazon(url):
    global session, headers
    html = session.get(url, headers=headers)
    bs = BeautifulSoup(html.text, 'html.parser')
    resultPage = bs.find('div', {'class': 's-main-slot s-result-list s-search-results sg-row'})
    top10 = dict()
    for i in range(10):
        try:
            result = resultPage.find('div', {'data-index': i})
        except AttributeError:
            print(f'Data index {i} non-existent! Moving on...')
        else:
            title = result.find('span', {'class': 'a-size-base-plug a-color-base a-text-normal'}).get_text()
            price = result.find('span', {'class': 'a-offscreen'}).get_text()
            top10[title] = price 
    return top10 
    
if __name__ == '__main__':
    compareFor('bra')
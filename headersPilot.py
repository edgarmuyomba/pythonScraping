import socks, socket 
import requests 
from bs4 import BeautifulSoup

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket 

session = requests.Session()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
 'Accept':'text/html,application/xhtml+xml,application/xml;'
 'q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.whatismybrowser.com/'
html = session.get(url, headers=headers)
bs = BeautifulSoup(html.text, 'html.parser')
print(bs.find('div', {'class': 'string-major'}).get_text())
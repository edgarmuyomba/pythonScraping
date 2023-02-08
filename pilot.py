from urllib.request import urlopen
from bs4 import BeautifulSoup 

html = urlopen('https://pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, 'html.parser')

names = bs.find_all('span', {'class': 'green'})

for name in names:
    print(name.get_text())
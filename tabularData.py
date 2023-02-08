from urllib.request import urlopen 
from bs4 import BeautifulSoup

html = urlopen('https://pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

rows = bs.find_all('tr', {'class': 'gift'})

giftDict = dict()
for row in rows:
    elements = row.find_all('td')
    giftDict[row['id']] = [element.get_text() for element in elements]

for i,j in giftDict.items():
    print(j[0],'\t',j[2])
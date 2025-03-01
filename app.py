import csv
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
url='https://listado.mercadolibre.com.mx/google-pixel-7#D[A:google%20pixel%207]]'

baseurl = 'https://listado.mercadolibre.com.mx/'

searchurl = input("Enter search term: ")
csvname = input("Enter csv name: ")
searchurl = searchurl.replace('-', '.').lower()
url = baseurl + searchurl
print(url)

r=requests.get(url,headers=headers)
print(r)

soup = BeautifulSoup(r.content, 'html.parser')

items=[]
print('aa')



#for item in soup.select('ui-search-layout ui-search-layout--stack shops__layout'):
for row in soup.find_all('ol', class_='ui-search-layout ui-search-layout--stack shops__layout'):
    cards = row.find_all('li', class_='ui-search-layout__item shops__layout-item')
    for card in cards:
        item = {}
        item['name'] = card.find( 'h3').text
        item['price'] = card.find( class_='poly-price__current').text.strip()
        item['url'] = card.find('a', class_ = 'poly-component__title')['href']
        item['img'] = card.find('img', class_='poly-component__picture')['src']
        discount_span = card.find('span', class_='andes-money-amount__discount')
        item['discount'] = discount_span.text.strip() if discount_span else 'N/A'
        items.append(item)
    if not cards:
        print('No cards found')

filename = csvname + '.csv'
with open(r'./data/' + filename, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f,['name','price','discount','url','img'])
    w.writeheader()
    for item in items:
        w.writerow(item)




with open(r"data/SOUP.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())


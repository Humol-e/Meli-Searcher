import csv
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

url = input("Enter url: ")
#csvname = input("Enter csv name: ")
csvname = "prueba"
r=requests.get(url,headers=headers)
print(r)

soup = BeautifulSoup(r.content, 'html.parser')

items=[]

for row in soup.find_all('div', class_='ui-pdp-container__row ui-pdp-with--separator--fluid ui-pdp-with--separator--40-24'):
    cards = row.find_all('div', class_='ui-pdp-container__col col-2 mr-24 mt-8')
    for card in cards:
        item = {}
        item['name'] = card.find('h1').text
        price = card.find('div', class_ = 'ui-pdp-container__row ui-pdp-container__row--price')
        if price:
            item['price'] = price.find('span', class_='andes-money-amount__fraction').text.strip()
        else:
            item['price'] = 'N/A'
        item['price'] = item['price'].replace('"', '').replace(',', '')
        items.append(item)
    if not cards:
        print('No cards found')

filename = csvname + '.csv'
with open(r'./data/' + filename, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f,['name','price'])
    w.writeheader()
    for item in items:
        w.writerow(item)

with open(r"data/item.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())


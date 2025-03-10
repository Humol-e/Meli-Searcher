import csv
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from PIL import Image
from io import StringIO
from io import BytesIO
# Configurar la interfaz de Streamlit
st.title('Price Tracker')
st.write('Enter the URL of the product page on MercadoLibre:')
newimg = st.empty()
# Entrada de URL y nombre del archivo CSV
url = st.text_input('Enter URL:')
csvname = st.text_input('Enter CSV name:', 'prueba')
dfempty = st.empty()
if st.button('Track Price'):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    r = requests.get(url, headers=headers)
    st.write(f'Status Code: {r.status_code}')

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        items = []

        for row in soup.find_all('div', class_='ui-pdp-container__row ui-pdp-with--separator--fluid ui-pdp-with--separator--40-24'):
            item = {}
            cards = row.find_all('div', class_='ui-pdp-container__col col-2 mr-24 mt-8')
            images = row.find_all('div', class_='ui-pdp-container__col col-2 ui-pdp--relative')
            for card in cards:
                
                item['name'] = card.find('h1').text
                price = card.find('div', class_ = 'ui-pdp-container__row ui-pdp-container__row--price')
                if price:
                    item['price'] = price.find('span', class_='andes-money-amount__fraction').text.strip()
                else:
                    item['price'] = 'N/A'
                item['price'] = item['price'].replace('"', '').replace(',', '')
            if not cards:
                print('No cards found')
            for img in images:
                print("ola")
                item['img'] = img.find('img', class_='ui-pdp-image ui-pdp-gallery__figure__image')['data-zoom']
                items.append(item)
            if not images:
                print('No images found')

        filename = csvname + '.csv'
        with open(r'./data/' + filename, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, ['name', 'price', 'img'])
            w.writeheader()
            for item in items:
                w.writerow(item)

        st.write(f'Data saved to {filename}')
        df = pd.read_csv(r'./data/' + filename)
        resizedImageUrl = df.iloc[-1]['img']
        st.write(resizedImageUrl)
        def load_image(resizedImageUrl):
            r = requests.get(resizedImageUrl)
            newimg = Image.open(BytesIO(r.content))
            newimg = newimg.resize((300, 300))
            return newimg
        load_image(resizedImageUrl)
        st.image(load_image(resizedImageUrl), width=300)    
        df['img'] = newimg
        dfempty.dataframe(df)

    else:
        st.write('Failed to retrieve the page.')


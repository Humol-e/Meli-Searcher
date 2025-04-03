import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# Streamlit app title and description
st.title("WEB Item Searcher")
st.write("Enter a search term to scrape product data from AliExpress and MercadoLibre.")

# Input fields for search term and CSV file name
searchurl = st.text_input("Enter search term:", "example")

# Base URL for AliExpress
alieBaseUrl = 'https://es.aliexpress.com/w/wholesale-'
alieUrl = alieBaseUrl + searchurl.replace('-', '.').lower() + '.html'

# Button to trigger the scraping process

# Button to trigger the scraping process
if st.button("Scrape Data"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }

    # Scraping para MercadoLibre
    r_ml = requests.get(alieUrl, headers=headers)
    print(f"Status Code: {r_ml.status_code}")
    if r_ml.status_code == 200:
        soup_ml = BeautifulSoup(r_ml.content, 'html.parser')
        items_ml = []
        for row in soup_ml.find_all('ol', class_='ui-search-layout ui-search-layout--stack shops__layout'):
            cards = row.find_all('li', class_='ui-search-layout__item shops__layout-item')
            for card in cards:
                item = {}
                item['name'] = card.find('h3').text
                price_span = card.find('span', class_='andes-money-amount__fraction')
                item['price'] = price_span.text.strip().replace(',', '') if price_span else 'N/A'
                item['img'] = card.find('img', class_='poly-component__picture')['src']
                item['url'] = card.find('a', class_='poly-component__title')['href']
                discount_span = card.find('span', class_='andes-money-amount__discount')
                item['discount'] = discount_span.text.strip() if discount_span else 'N/A'
                items_ml.append(item)

    # Scraping para AliExpress
    r_ae = requests.get(alieUrl, headers=headers)
    print(f"Status Code: {r_ae.status_code}")
    if r_ae.status_code == 200:
        soup_ae = BeautifulSoup(r_ae.content, 'html.parser')
        items_ae = []
        for row in soup_ae.find_all('div', class_='hs_ht'):
            cards = row.find_all('div', class_='hs_bw search-item-card-wrapper-gallery')
            for card in cards:
                item = {}
                nameDiv = card.find('div', class_='l5_ag')
                item['name'] = nameDiv.get('title') if nameDiv else 'N/A'
                price = card.find('div', class_='l5_k6')
                item['price'] = price.text.strip().replace('"', '').replace(',', '') if price else 'N/A'
                urlDiv = card.find('a', class_='l5_b io_it search-card-item')
                shopUrl = card.find('span', class_='io_ip')
                item['shop'] = shopUrl.text.strip() if shopUrl else 'N/A'
                img = card.find('img', class_='ml_bg')
                item['img'] = img['src'] if img else 'N/A'
                item['url'] = urlDiv.get('href') if urlDiv else 'N/A'

                items_ae.append(item)

    # Mostrar los dataframes en columnas distintas
    col1, col2 = st.columns(2)
    with col1:
        st.write("MercadoLibre")
        df_ml = pd.DataFrame(items_ml)
        st.data_editor(
            df_ml,
            column_config={
                "img": st.column_config.ImageColumn(),
                "url": st.column_config.LinkColumn("URL")
            },
            hide_index=True,
        )
    with col2:
        st.write("AliExpress")
        df_ae = pd.DataFrame(items_ae)
        st.data_editor(
            df_ae,
            column_config={
                "img": st.column_config.ImageColumn(),
                "url": st.column_config.LinkColumn("URL")
            },
            hide_index=True,
        )
    
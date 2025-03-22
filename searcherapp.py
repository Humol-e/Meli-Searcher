import csv
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# Streamlit app title and description
st.title("MercadoLibre Item Searcher")
st.write("Enter a search term to scrape product data from MercadoLibre.")

# Input fields for search term and CSV file name
searchurl = st.text_input("Enter search term:", "google-pixel-7")
csvname = st.text_input("Enter CSV name:", "output")

# Base URL for MercadoLibre
baseurl = 'https://listado.mercadolibre.com.mx/'
url = baseurl + searchurl.replace('-', '.').lower()

# Button to trigger the scraping process
if st.button("Scrape Data"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }
    r = requests.get(url, headers=headers)
    print(f"Status Code: {r.status_code}")

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        items = []

        # Scraping logic
        for row in soup.find_all('ol', class_='ui-search-layout ui-search-layout--stack shops__layout'):
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
                items.append(item)
                float(item['price'])
        # Check if items were found
        if not items:
            st.write("No items found.")
        else:
            # Display data in a table
            df = pd.DataFrame(items)
            df['price'] = df['price'].astype(float)

            st.data_editor(
                df,
                column_config={
                    "img": st.column_config.ImageColumn(),

                    "url": st.column_config.LinkColumn("URL")
                },
                hide_index=True,
            )




    else:
        st.write("Failed to retrieve the page. Please check the URL or try again later.")
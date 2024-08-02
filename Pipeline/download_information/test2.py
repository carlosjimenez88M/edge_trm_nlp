

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import argparse
import logging
import re


# url = 'https://cnnespanol.cnn.com/'
# r = requests.get(url)
# soup = BeautifulSoup(r.text,"html5lib")
#
#
#
#
#
#
#
#
# Extracción de urls  ----------
import requests
from bs4 import BeautifulSoup
import pandas as pd

class CNNNewsExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.soup = None

    def _fetch_content(self):
        try:
            r = requests.get(self.base_url)
            self.soup = BeautifulSoup(r.text, "html5lib")
        except requests.RequestException as e:
            print(f"Failed to fetch content from {self.base_url}: {e}")
            self.soup = None

    def extract_title(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html5lib")
            title = soup.find('h1').get_text(strip=True)
            return title
        except Exception as e:
            print(f"Not found Title in this URL {url}: {e}")
            return None

    def extract_content(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html5lib")
            main_content = soup.find_all('p')
            texts = [element.get_text(strip=True) for element in main_content]
            full_text = ' '.join(texts)
            return full_text
        except Exception as e:
            print(f"Failed to extract content from {url}: {e}")
            return None

    def extract_urls(self):
        if self.soup is None:
            self._fetch_content()

        if self.soup:
            all_urls = self.soup.find_all('a', class_='news__media-item')
            urls = [url.get('href') for url in all_urls]
            return urls
        else:
            return []

    def cnn_news(self):
        try:
            urls = self.extract_urls()
            print('Total urls are', len(urls), 'this is one example')
            if urls:
                print(urls[0])

            df = pd.DataFrame(urls, columns=['Link'])
            df['Titulo'] = df['Link'].apply(lambda x: self.extract_title(x))
            df['Contenido'] = df['Link'].apply(lambda x: self.extract_content(x))
            print(df.head())
            print()
            print(df['Contenido'].head(1))
            return df
        except Exception as e:
            print(f"Failed to extract news: {e}")
            return pd.DataFrame(columns=['Link', 'Titulo', 'Contenido'])

# Ejemplo de uso
base_url = "https://cnnespanol.cnn.com/"
extractor = CNNNewsExtractor(base_url)
news_df = extractor.cnn_news()

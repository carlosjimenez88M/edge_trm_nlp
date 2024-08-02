'''
Main Class to Scrap information to CNN in Spanish
@ Author: Carlos Daniel Jiménez Martinez
@ 2024
'''



# Libraries ----------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# Main Class ---------
class CNNNewsExtractor:
    """
    A class to extract news articles, titles, and contents from CNN Español.

    Attributes:
        base_url (str): The base URL of the CNN Español website.
        soup (BeautifulSoup): The BeautifulSoup object for parsing HTML content.
        download_date (str): The date when the data was downloaded.
    """

    def __init__(self, base_url):
        """
        Initializes the CNNNewsExtractor with the base URL.

        Args:
            base_url (str): The base URL of the CNN Español website.
        """
        self.base_url = base_url
        self.soup = None
        self.download_date = datetime.now().strftime("%Y-%m-%d")

    def _fetch_content(self):
        """
        Fetches and parses the HTML content from the base URL.
        """
        try:
            r = requests.get(self.base_url)
            self.soup = BeautifulSoup(r.text, "html5lib")
        except requests.RequestException as e:
            print(f"Failed to fetch content from {self.base_url}: {e}")
            self.soup = None

    def extract_title(self, url):
        """
        Extracts the title from a given news article URL.

        Args:
            url (str): The URL of the news article.

        Returns:
            str: The title of the article, or None if not found.
        """
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html5lib")
            title = soup.find('h1').get_text(strip=True)
            return title
        except Exception as e:
            print(f"Not found Title in this URL {url}: {e}")
            return None

    def extract_content(self, url):
        """
        Extracts the content from a given news article URL.

        Args:
            url (str): The URL of the news article.

        Returns:
            str: The full text content of the article, or None if not found.
        """
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
        """
        Extracts all news article URLs from the base URL.

        Returns:
            list: A list of URLs found on the base URL page.
        """
        if self.soup is None:
            self._fetch_content()

        if self.soup:
            all_urls = self.soup.find_all('a', class_='news__media-item')
            urls = [url.get('href') for url in all_urls]
            return urls
        else:
            return []

    def cnn_news(self):
        """
        Extracts news URLs, titles, and contents and stores them in a DataFrame.

        Returns:
            DataFrame: A pandas DataFrame containing the news URLs, titles, and contents.
        """
        try:
            urls = self.extract_urls()
            print('Total URLs are', len(urls), 'this is one example')
            if urls:
                print(urls[0])

            df = pd.DataFrame(urls, columns=['Link'])
            df['Title'] = df['Link'].apply(lambda x: self.extract_title(x))
            df['Content'] = df['Link'].apply(lambda x: self.extract_content(x))
            df['Download_Date'] = self.download_date
            print(df.head())
            return df
        except Exception as e:
            print(f"Failed to extract news: {e}")
            return pd.DataFrame(columns=['Link', 'Title', 'Content', 'Download_Date'])
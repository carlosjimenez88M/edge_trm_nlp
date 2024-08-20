"""
Infobae Web Scraping Utilities
Contains functions for scraping Infobae articles.
@2024
"""

# Libraries ------------
import requests
from bs4 import BeautifulSoup
import logging

# Logger configuration
logging.basicConfig(
    filename='../../logs/infobae_functions.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def initial_validation(url):
    """
    Validates the initial request to a given URL and parses the content using BeautifulSoup.

    Args:
        url (str): The URL to be validated.

    Returns:
        BeautifulSoup object if the URL is valid and the content is parsed successfully, otherwise None.
    """
    try:
        logger.info(f'Starting request for URL: {url}')
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html5lib')
        logger.info(f'Successfully validated and parsed URL: {url}')
        return soup
    except requests.RequestException as e:
        logger.error(f'Failed to request the URL {url}: {e}')
        return None


def extract_titles(soup):
    """
    Extracts titles from the parsed HTML content.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        list: A list of titles extracted from the HTML content.
    """
    logger.info('Extracting titles...')
    try:
        titles = [title.get_text(strip=True)
                  for title in soup.find('div').find_all('h2', class_='story-card-hl')]
        logger.info(f'Extracted {len(titles)} titles.')
        return titles
    except Exception as e:
        logger.error(f'Error extracting titles: {e}')
        return []


def extract_urls(soup):
    """
    Extracts article URLs from the parsed HTML content.

    Args:
        soup (BeautifulSoup): Parsed HTML content.

    Returns:
        list: A list of article URLs extracted from the HTML content.
    """
    logger.info('Extracting URLs...')
    try:
        urls = ['https://www.infobae.com/' + url.get('href')
                for url in soup.find('div').find_all('a', class_='headline-link')]
        logger.info(f'Extracted {len(urls)} URLs.')
        return urls
    except Exception as e:
        logger.error(f'Error extracting URLs: {e}')
        return []


def get_content(url):
    """
    Extracts the content of an article from a given URL.

    Args:
        url (str): URL of the article.

    Returns:
        str: The content of the article or an error message.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        article = soup.find(class_='article')
        if article:
            return article.get_text(strip=True)\
                .replace('ESTGuardarNuevoEl', '')\
                .replace('ESTGuardarNuevoImagen', '')\
                .replace('ESTGuardarNuevoLa', '').strip()
        else:
            return "No article content found"
    except Exception as e:
        return f"Error: {e}"


def get_date(url):
    """
    Extracts the publication date of an article from a given URL.

    Args:
        url (str): URL of the article.

    Returns:
        str: The publication date or an error message.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        dates = soup.find(class_='sharebar-article-date')
        if dates:
            return dates.get_text(strip=True)
        else:
            return "No dates content found"
    except Exception as e:
        return f"Error: {e}"


def get_author(url):
    """
    Extracts the author's name of an article from a given URL.

    Args:
        url (str): URL of the article.

    Returns:
        str: The author's name or an error message.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        authors = soup.find(class_='author-name')
        if authors:
            return authors.get_text(strip=True)
        else:
            return "No author found"
    except Exception as e:
        return f"Error: {e}"

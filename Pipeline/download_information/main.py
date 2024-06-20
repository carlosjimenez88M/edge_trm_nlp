#========================================#
#          Google News Scrapper          #
#          edge_trm_nlp project          #
#========================================#


# Description ------------------
#


# Todo --------------------------




# Libraries --------------------
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
import argparse
import logging
import re

# Logger Configuration ---------------

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)

# Logger Configuration ---------------
logging.basicConfig(
    filename=os.path.join(log_dir, 'download_data.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()



def go(args):
    timezone = args.timezone
    logger.info('Starting go function with timezone: %s', timezone)
    try:
        url = args.url_news
        r = requests.get(url)
        r.raise_for_status()
        logger.info('Successfully fetched the URL: %s', url)
    except requests.RequestException as e:
        logger.error('Error fetching the URL: %s, Error: %s', url, e)
        return pd.DataFrame()

    soup = BeautifulSoup(r.text, 'html5lib')
    logger.info('Initialized Web Scrapping Process')

    news_links = soup.find_all('a', class_='gPFEn')
    sources = soup.find_all('div', class_='MCAGUe')
    times = soup.find_all('time', class_='hvbAAd')

    num_items = min(len(news_links), len(sources), len(times))
    logger.info('Found %d items to process', num_items)

    data = []

    local_tz = pytz.timezone(timezone)
    logger.info('Extracting titles, sources, and datetimes')
    for i in range(num_items):
        try:
            title = news_links[i].get_text(strip=True).strip()
            source = sources[i].get_text(strip=True).replace('Más', '').strip()

            full_datetime = times[i]
            lag_time_text = full_datetime.get_text(strip=True)
            lag_time_match = re.findall(r'\d+', lag_time_text)

            if lag_time_match:
                lag_time = int(lag_time_match[0])
                datetime_local = datetime.now(local_tz)
                time_diff = timedelta(hours=lag_time)
                publication_time = datetime_local - time_diff
                time_part = publication_time.time().strftime("%H:%M:%S")
            else:
                time_part = "N/A"

            data.append({
                'Title': title,
                'Source': source,
                'Publication Time': time_part
            })
            logger.debug('Processed item: %s', title)
        except Exception as e:
            logger.error('Error processing item %d: %s', i, e)

    logger.info('Extracting authors')
    author_divs = soup.find_all('div', class_='bInasb')
    author_dict = {}
    for div in author_divs:
        try:
            parent = div.find_parent('article')
            if parent:
                link = parent.find('a', class_='gPFEn')
                if link:
                    key = link.get_text(strip=True)
                    author_dict[key] = div.get_text(strip=True)
                    logger.debug('Author found for title: %s', key)
        except Exception as e:
            logger.error('Error extracting author: %s', e)

    logger.info('Matching titles with authors')
    for item in data:
        item['Author'] = author_dict.get(item['Title'], None)
        if item['Author'] is None:
            logger.debug('No author found for title: %s', item['Title'])

    df = pd.DataFrame(data)
    logger.info('DataFrame created with %d rows', len(df))
    return df

def save_to_parquet_file(df, args, filename=None):
    logger.info('Starting save_to_parquet_file function')
    save_directory = args.save_directory
    os.makedirs(save_directory, exist_ok=True)
    logger.info('Directory %s created if it did not exist', save_directory)

    if filename is None:
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f'{save_directory}/{current_date}_news_data.parquet'

    try:
        df.to_parquet(filename, index=False)
        logger.info('DataFrame successfully saved to %s', filename)
    except Exception as e:
        logger.error('Error saving DataFrame to %s: %s', filename, e)

if __name__ == '__main__':
    logger.info('Program started')
    parser = argparse.ArgumentParser(
        description='News Scrapping Artifact'
    )
    parser.add_argument(
        "--timezone",
        type=str,
        help="Time Zone (into the project)",
        required=True
    )
    parser.add_argument(
        "--artifact_name",
        type=str,
        help="Name for the artifact",
        required=True
    )

    parser.add_argument(
        "--url_news",
        type=str,
        help="URL to the input file",
        required=True
    )

    parser.add_argument(
        "--save_directory",
        type=str,
        help="Path to save dataframe",
        required=True
    )

    args = parser.parse_args()

    df = go(args)
    if not df.empty:
        save_to_parquet_file(df, args=args)
        print(df.head(15))
    else:
        logger.error('No data to save, exiting program')
    logger.info('Program finished')



## Libraries -----------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
import argparse
import os


#Logger Configuration ---------------

log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'dolar_scraping.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()


def save_to_parquet_file(df, args, filename=None):
    logger.info('Starting save_to_parquet_file function')
    save_directory = args.save_directory
    os.makedirs(save_directory, exist_ok=True)
    logger.info('Directory %s created if it did not exist', save_directory)

    if filename is None:
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f'{save_directory}/news_data_{current_date}.parquet'

    try:
        df.to_parquet(filename, index=False)
        logger.info('DataFrame successfully saved to %s', filename)
    except Exception as e:
        logger.error('Error saving DataFrame to %s: %s', filename, e)


def go(args):
    try:
        logger.info('Starting exchange rate extraction process.')
        r = requests.get(args.url_dolar)
        r.raise_for_status()
        logger.info('Successfully fetched the URL content.')

        soup = BeautifulSoup(r.text, 'html5lib')
        dolar = soup.find('div', class_='valores trm')

        if dolar:
            exchange_rate = dolar.get_text(strip=True).replace('TRM','')
            logger.info(f'Exchange Rate extracted: {exchange_rate}')
        else:
            exchange_rate = None
            logger.warning('No exchange rate found.')

        current_datetime = datetime.now()
        data = {
            'Date': [current_datetime.date()],
            'Hour': [current_datetime.time()],
            'Exchange_rate': [exchange_rate]
        }

        df = pd.DataFrame(data)
        logger.info('DataFrame created with the extracted data.')
        print(df)

        current_date_str = current_datetime.strftime('%Y-%m-%d')
        filename = f'{args.save_directory}/{current_date_str}_exchange_rate.parquet'

        save_to_parquet_file(df, args, filename)


    except requests.exceptions.RequestException as e:
        logger.error(f'Error fetching the URL content: {e}')
    except Exception as e:
        logger.error(f'An error occurred: {e}', exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract exchange rate and save to Parquet file.')
    parser.add_argument('--url_dolar',
                        type=str,
                        required=True,
                        help='URL of the page to scrape the exchange rate from')
    parser.add_argument('--save_directory',
                        type=str,
                        required=True,
                        help='Directory to save the Parquet file')
    args = parser.parse_args()
    go(args)



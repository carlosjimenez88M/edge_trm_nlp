'''
This script scrapes the exchange rate from a given URL, stores the scraped data (date, time, exchange rate)
in a Pandas DataFrame, and saves the data in a Parquet file. The filename of the Parquet file includes
the current date and time of the download, ensuring uniqueness.

Logging is implemented to track the progress and potential issues during the execution of the script,
including fetching the URL content, extracting the exchange rate, saving the data, and error handling.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
import argparse
import os

# Logger Configuration ---------------
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'dolar_scraping.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def save_to_parquet_file(df, save_directory, filename=None):
    """
    Save the given DataFrame to a Parquet file. The filename will include the current date and time.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
        save_directory (str): The directory where the Parquet file will be saved.
        filename (str, optional): The filename to use. If not provided, a default based on the date and time will be used.

    Raises:
        Exception: If there is an issue saving the DataFrame, it logs the error and raises the exception.
    """
    logger.info('Starting save_to_parquet_file function.')
    os.makedirs(save_directory, exist_ok=True)
    logger.info('Directory %s created if it did not exist.', save_directory)

    try:
        if filename is None:
            current_datetime = datetime.now()
            current_date_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'{save_directory}/exchange_rate_{current_date_str}.parquet'

        df.to_parquet(filename, index=False)
        logger.info('DataFrame successfully saved to %s.', filename)
    except Exception as e:
        logger.error('Error saving DataFrame to %s: %s', filename, e)
        raise


def go(args):
    """
    Main function that handles the process of fetching the exchange rate, extracting it, storing it in a DataFrame,
    and saving the DataFrame as a Parquet file.

    Args:
        args (argparse.Namespace): Arguments passed to the script including URL and save directory.
    """
    try:
        logger.info('Starting exchange rate extraction process.')

        response = requests.get(args.url_dolar)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        logger.info('Successfully fetched the URL content.')

        soup = BeautifulSoup(response.text, 'html5lib')
        dolar = soup.find('div', class_='valores trm')

        if dolar:
            exchange_rate = dolar.get_text(strip=True).replace('TRM', '')
            logger.info('Exchange rate extracted: %s', exchange_rate)
        else:
            exchange_rate = None
            logger.warning('No exchange rate found.')

        current_datetime = datetime.now()
        data = {
            'Date': [current_datetime.date()],
            'Hour': [current_datetime.strftime('%H:%M:%S')],
            'Exchange_rate': [exchange_rate]
        }

        df = pd.DataFrame(data)
        logger.info('DataFrame created with the extracted data.')
        print(df)


        current_datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{args.save_directory}/{current_datetime_str}_exchange_rate.parquet'

        save_to_parquet_file(df, args.save_directory, filename)

    except requests.exceptions.RequestException as e:
        logger.error('Error fetching the URL content: %s', e)
    except Exception as e:
        logger.error('An unexpected error occurred: %s', e, exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract exchange rate and save to Parquet file.')
    parser.add_argument(
        '--url_dolar',
        type=str,
        required=True,
        help='URL of the page to scrape the exchange rate from'
    )
    parser.add_argument(
        '--save_directory',
        type=str,
        required=True,
        help='Directory to save the Parquet file'
    )
    args = parser.parse_args()
    go(args)

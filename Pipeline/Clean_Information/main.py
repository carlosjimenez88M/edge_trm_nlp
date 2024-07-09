"""
Clean process artifacts
2024-07-08
"""

import os
import logging
import pandas as pd
from utils import clean_titles, clean_author, clean_time, clean_value
from datetime import datetime

# Configure logger
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'clean_data.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def find_latest_file(data_dir, keyword):
    """
    Find the latest file in the specified directory containing the given keyword by date.

    Args:
        data_dir (str): Directory to search for files.
        keyword (str): Keyword to match filenames.

    Returns:
        str: Path to the latest file.
    """
    try:
        files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if keyword in f]
        if not files:
            raise FileNotFoundError(f"No files found in {data_dir} containing keyword {keyword}")

        # Extract date from filenames and find the most recent one
        latest_file = max(files, key=lambda x: datetime.strptime(os.path.basename(x).split('_')[0], '%Y-%m-%d'))
        return latest_file
    except Exception as e:
        logger.error(f"Error finding the latest file: {e}")
        raise

def main():
    """
    Main function to clean news and exchange rate data and save the cleaned data.
    """
    try:
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
        clean_data_dir = os.path.abspath(os.path.join(data_dir, 'data_clean'))
        os.makedirs(clean_data_dir, exist_ok=True)

        # Find the latest news and exchange rate files
        news_file = find_latest_file(data_dir, 'news_data')
        exchange_rate_file = find_latest_file(data_dir, 'exchange_rate')

        # Extract date from filenames
        news_date = os.path.basename(news_file).split('_')[0]
        exchange_rate_date = os.path.basename(exchange_rate_file).split('_')[0]

        # Load data
        news = pd.read_parquet(news_file)
        exchange_rate = pd.read_parquet(exchange_rate_file)

        # Clean data for news
        if 'Title' in news.columns:
            news['Cleaned_Title'] = clean_titles(news)
        else:
            logger.warning("Column 'Title' not found in news data")

        if 'Author' in news.columns:
            news['Cleaned_Author'] = news['Author'].apply(clean_author)
        else:
            logger.warning("Column 'Author' not found in news data")

        # Clean data for exchange rate
        if 'Hour' in exchange_rate.columns:
            exchange_rate['Cleaned_Hour'] = exchange_rate['Hour'].apply(clean_time)
        else:
            logger.warning("Column 'Hour' not found in exchange rate data")

        if 'Exchange_rate' in exchange_rate.columns:
            exchange_rate['Cleaned_Exchange_rate'] = exchange_rate['Exchange_rate'].apply(clean_value)
        else:
            logger.warning("Column 'Exchange_rate' not found in exchange rate data")

        # Save cleaned data with date in filenames
        news_cleaned_path = os.path.join(clean_data_dir, f'{news_date}_cleaned_news_data.parquet')
        exchange_rate_cleaned_path = os.path.join(clean_data_dir, f'{exchange_rate_date}_cleaned_exchange_rate.parquet')

        news.to_parquet(news_cleaned_path)
        print(news.head())
        exchange_rate.to_parquet(exchange_rate_cleaned_path)
        print(exchange_rate.head())

        logger.info("Data cleaned and saved successfully.")

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()

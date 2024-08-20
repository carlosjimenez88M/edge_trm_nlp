"""
Infobae Web Scraping Main Script
This script scrapes articles from Infobae and stores the data in a Parquet file.
@2024
"""

# Libraries ------------
import argparse
import pandas as pd
from datetime import datetime
from utils import initial_validation, extract_titles, extract_urls, get_content, get_date, get_author
import logging

# Configuración del logger
logging.basicConfig(
    filename='../../logs/infobae_download_data.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def go(url: str, save_directory: str):
    """
    Main function that executes the web scraping process for the given URL and saves the results to a Parquet file.

    Args:
        url (str): The URL to be processed.
        save_directory (str): The destination path to save the Parquet file.
    """
    logger.info(f'Starting web scraping process for URL: {url}')

    try:
        soup = initial_validation(url)
        if soup is None:
            logger.error(f'Failed to validate the URL: {url}')
            print(f"Failed to validate the URL: {url}")
            return

        titles = extract_titles(soup)
        urls = extract_urls(soup)

        if len(titles) != len(urls):
            logger.error("The length of titles and URLs do not match.")
            print("The length of titles and URLs do not match.")
            return

        df = pd.DataFrame({
            'URL': urls,
            'Title': titles
        })


        df['Content'] = df['URL'].apply(get_content)
        df['Date'] = df['URL'].apply(get_date)
        df['Author'] = df['URL'].apply(get_author)
        print(df.head())

        current_date = datetime.now().strftime('%Y-%m-%d')
        file_name = f'infobae_{current_date}.parquet'
        output_path = f'{save_directory}/{file_name}'
        df.to_parquet(output_path, index=False)

        logger.info(f'Data successfully saved to {output_path}')
        print(f"Data successfully saved to {output_path}")

    except Exception as e:
        logger.error(f'An error occurred during the scraping process: {e}')
        print(f"An error occurred: {e}")


def main():
    """
    Main function that parses arguments and triggers the web scraping process.
    """
    parser = argparse.ArgumentParser(description="Infobae Web Scraping Tool")

    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='The URL of the article to scrape'
    )

    parser.add_argument(
        '--save_directory',
        type=str,
        required=True,
        help='The destination path where the Parquet file will be saved'
    )

    args = parser.parse_args()

    go(args.url, args.save_directory)


if __name__ == "__main__":
    main()

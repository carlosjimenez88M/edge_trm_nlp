'''
Orchestrator of the News Scraping Model
Schema that generates the news database at a high level
@ Autor: Carlos Daniel Jiménez
@ 2024
'''
import argparse
import logging
import os
from cnn_extractor.extractor import CNNNewsExtractor
from datetime import datetime
from omegaconf import OmegaConf

# Logger Configuration
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'download_data.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


def main(base_url, save_directory):
    """
    Main function to run the CNNNewsExtractor.

    Args:
        base_url (str): The base URL of the CNN Español website.
        save_directory (str): The directory to save the extracted news data.
    """
    logger.info('Starting CNN News Extractor')

    extractor = CNNNewsExtractor(base_url)
    logger.info(f'Initialized CNNNewsExtractor with base URL: {base_url}')

    try:
        news_df = extractor.cnn_news()
        logger.info(f'Extracted news dataframe with {len(news_df)} records')

        # Save the dataframe with the current date as the filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), save_directory))
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"news_{date_str}.parquet")
        news_df.to_parquet(output_file, index=False)

        logger.info(f'Saved news dataframe to {output_file}')
        print(f'Saved news dataframe to {output_file}')
    except Exception as e:
        logger.error(f'Failed to extract news: {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract news from CNN Español.')
    parser.add_argument('--base_url',
                        type=str,
                        help='The base URL of the CNN Español website.')
    parser.add_argument('--save_directory',
                        type=str,
                        help='The directory to save the extracted news data.')
    args = parser.parse_args()

    logger.info('Parsing arguments')
    main(args.base_url, args.save_directory)
    logger.info('Finished CNN News Extraction')

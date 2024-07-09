import os
import re
import logging
import pandas as pd
from nltk.corpus import stopwords

# Configure logger
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'clean_data.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

stop_words = set(stopwords.words("spanish"))

def clean_titles(df):
    """
    Clean the titles in the DataFrame by removing stop words and special characters.

    Args:
        df (pd.DataFrame): DataFrame containing a 'Title' column.

    Returns:
        pd.Series: Series with cleaned titles.
    """
    try:
        def clean_text(text):
            text = re.sub(r'[^\w\s]', '', text)
            return text

        filtered_titles = df['Title'].apply(lambda title: ' '.join(
            [w for w in clean_text(title).split() if w.lower() not in stop_words]
        ))
        return filtered_titles
    except Exception as e:
        logger.error(f"Error cleaning titles: {e}")
        raise

def clean_author(author):
    """
    Clean the author names by removing duplication and specific patterns.

    Args:
        author (str): Author name string.

    Returns:
        str: Cleaned author name.
    """
    try:
        if not author:
            return author

        pattern = re.compile(r'(.*?)De\s\1', re.IGNORECASE)
        author = re.sub(pattern, r'\1', author)

        words = author.split()
        half_length = len(words) // 2
        if words[:half_length] == words[half_length:]:
            return ' '.join(words[:half_length])

        return author
    except Exception as e:
        logger.error(f"Error cleaning author: {e}")
        raise

def clean_time(time_obj):
    """
    Clean the time by removing microseconds.

    Args:
        time_obj (datetime.time): Time object.

    Returns:
        str: Cleaned time in HH:MM:SS format.
    """
    try:
        return time_obj.strftime('%H:%M:%S')
    except Exception as e:
        logger.error(f"Error cleaning time: {e}")
        raise

def clean_value(value_str):
    """
    Clean the monetary value by removing the dollar sign and decimals.

    Args:
        value_str (str): Monetary value string.

    Returns:
        int: Cleaned integer value.
    """
    try:
        value_str = value_str.replace('$', '').replace('.', '')
        value_str = value_str.split(',')[0]
        return int(value_str)
    except Exception as e:
        logger.error(f"Error cleaning value: {e}")
        raise

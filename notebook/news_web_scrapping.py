#=============================================#
#    Raspberry Pi Time series and NLP Project #
#          Google News Web Scrapping          #
#            Carlos Daniel Jiménez            #
#                   2024                      #
#=============================================#


# Description ----------------
# The principal goal in this script is create a program to scrap from google news  
# 


# Libraries --------------------
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pytz


def go(timezone='America/Bogota'):
    url = 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVAB?hl=es-419&gl=CO&ceid=CO%3Aes-419'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html5lib')

    news_links = soup.find_all('a', class_='gPFEn')
    sources = soup.find_all('div', class_='MCAGUe')
    times = soup.find_all('time', class_='hvbAAd')

    num_items = min(len(news_links), len(sources), len(times))

    data = []

    local_tz = pytz.timezone(timezone)

    for i in range(num_items):
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

    df = pd.DataFrame(data)
    return df

def save_to_parquet_file(df, filename=None):
    save_directory = '/mnt/external/Raspberry/news_project'
    os.makedirs(save_directory, exist_ok=True)

    if filename is None:
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f'{save_directory}/news_data_{current_date}.parquet'

    # Guardar el DataFrame en formato Parquet
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    df = go()
    save_to_parquet_file(df)
    print(df.head(15))







#### Todo ----------------

## URL
#print('=='*32)
#urls=  soup.find_all('div',class_='bInasb')
#for link in soup.find_all('a'):
#    print(link.get('href'))
#print(urls[0]['href'])


# Hacer un Yml para los paths y las configuraciones de las corridas
# Extraer URL
# Extraer Autor
# Arreglar que cuando salga ayer en el tiempo hacer una resta de 24 horas.


#ls /mnt/external/Raspberry/news_project
#pip install pandas requests beautifulsoup4 html5lib pytz
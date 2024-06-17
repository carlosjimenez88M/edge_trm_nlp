#=============================================#
#    Raspberry Pi Time series and NLP Project #
#          Google News Web Scrapping          #
#            Carlos Daniel Jiménez            #
#                   2024                      #
#=============================================#


# Description ----------------
#
#


# Libraries --------------------
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pytz




## Program ------------------

url = 'https://news.google.com/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRFZxYUdjU0JtVnpMVFF4T1JvQ1EwOG9BQVAB?hl=es-419&gl=CO&ceid=CO%3Aes-419'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html5lib')


## Title
news_links = soup.find_all('a', class_='gPFEn')
#print(news_links)

print('=='*32)
print(news_links[0].get_text(strip=True).strip())

## Source
print('=='*32)
sources= soup.find_all('div',class_='MCAGUe')
print(sources[0].get_text(strip=True).replace('Más','').strip())


## Publication time
print('=='*32)
times= soup.find_all('time', class_='hvbAAd')
full_datetime = times[0]
lag_time = full_datetime.get_text(strip=True)
lag_time = int(re.findall(r'\d+', lag_time)[0])
#print(lag_time)


local_tz = pytz.timezone('America/Bogota')  # Adjust to your local timezone
datetime_local = datetime.now(local_tz)
time_diff = timedelta(hours=lag_time)
hms_news = datetime_local- time_diff
print(hms_news.time().strftime("%H:%M:%S"))
print()




### Function ------------

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

        # Verificar si se encontró un número en lag_time_text
        if lag_time_match:
            lag_time = int(lag_time_match[0])
            datetime_local = datetime.now(local_tz)
            time_diff = timedelta(hours=lag_time)
            publication_time = datetime_local - time_diff
            time_part = publication_time.time().strftime("%H:%M:%S")
        else:
            time_part = "N/A"  # Si no se encuentra un número, asignar un valor predeterminado


        data.append({
            'Title': title,
            'Source': source,
            'Publication Time': time_part
        })


    df = pd.DataFrame(data)
    return df

def quote(value):
    return f"""'{str(value).replace("'", "''")}'"""

def save_to_sql_file(df, filename=None):
    if filename is None:
        # Generar el nombre del archivo con la fecha actual
        current_date = datetime.now().strftime('%Y-%m-%d')
        filename = f'news_data_{current_date}.sql'

    with open(filename, 'w') as f:
        f.write('CREATE TABLE IF NOT EXISTS news (\n')
        f.write('    title TEXT PRIMARY KEY,\n')
        f.write('    source TEXT,\n')
        f.write('    publication_time TEXT,\n')
        f.write(');\n\n')

        for index, row in df.iterrows():
            f.write('INSERT INTO news (title, source, publication_time, url) VALUES (\n')
            f.write(f"    {quote(row['Title'])},\n")
            f.write(f"    {quote(row['Source'])},\n")
            f.write(f"    {quote(row['Publication Time'])},\n")
            f.write(');\n')

if __name__ == '__main__':
    df = go()
    save_to_sql_file(df)

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



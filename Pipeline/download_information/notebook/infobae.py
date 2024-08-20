'''
Infobae web scraping modelling 
'''


# libraries ------------
import requests
from bs4 import BeautifulSoup
import pandas as pd

# module------- 
r = requests.get('https://www.infobae.com/colombia/')
soup = BeautifulSoup(r.text, 'html5lib')

#print(soup.find('h2').get_text(strip=True))



# Title
titles= []
for h2_tag in soup.find('div').find_all('h2',class_='story-card-hl'):
    #print(h2_tag.get_text(strip=True))
    titles.append(h2_tag.get_text(strip=True))

# Url
urls = []
for url in soup.find('div').find_all('a',class_='headline-link'):
    #print('https://www.infobae.com/' + url.get('href'))
    urls.append('https://www.infobae.com/' + url.get('href'))

## Content -----
def get_content(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib')
        article = soup.find(class_='article')
        if article:
            return article.get_text(strip=True)\
                .replace('ESTGuardarNuevoEl','')\
                .replace('ESTGuardarNuevoImagen','')\
                .replace('ESTGuardarNuevoLa','').strip()
        else:
            return "No article content found"
    except Exception as e:
        return f"Error: {e}"

print(f"Number of titles: {len(titles)}")
print(f"Number of urls: {len(urls)}")

df = pd.DataFrame({
    'URL': urls,
    'Title': titles
})
#df['Content'] = df['URL'].apply(get_content)

## Fecha ---------

def get_date(url):
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

df['Date'] = df['URL'].apply(get_date)


## Author ---------


def get_author(url):
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


df['Author'] = df['URL'].apply(get_author)

print(df.head())


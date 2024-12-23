import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Configuración del WebDriver
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecuta en segundo plano
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/path/to/chromedriver")  # Cambia la ruta al ejecutable de chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Buscar enlaces de productos en Google
def buscar_enlaces_google(producto, max_enlaces=5):
    logger.info("Buscando enlaces en Google...")
    driver = iniciar_driver()
    driver.get("https://www.google.com")
    barra_busqueda = driver.find_element(By.NAME, "q")
    barra_busqueda.send_keys(producto)
    barra_busqueda.send_keys(Keys.RETURN)
    time.sleep(2)

    resultados = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
    enlaces = [resultado.get_attribute("href") for resultado in resultados[:max_enlaces]]
    driver.quit()

    logger.info(f"Encontrados {len(enlaces)} enlaces.")
    return enlaces

# Extraer información de precios desde una página web
def extraer_precios(enlace):
    logger.info(f"Extrayendo precios desde: {enlace}")
    try:
        response = requests.get(enlace, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ejemplo de extracción: Busca texto con el símbolo de moneda
        precios = []
        for precio in soup.find_all(string=lambda text: "$" in text or "S/." in text):
            precios.append(precio.strip())

        return precios
    except Exception as e:
        logger.error(f"Error al extraer precios: {e}")
        return []

# Programa principal
if __name__ == "__main__":
    producto = "Laptop Dell Inspiron"
    try:
        logger.info(f"Buscando mejores precios para: {producto}")
        enlaces = buscar_enlaces_google(producto)

        precios_totales = []
        for enlace in enlaces:
            precios = extraer_precios(enlace)
            if precios:
                precios_totales.extend(precios)

        logger.info(f"Precios encontrados: {precios_totales}")
    except Exception as e:
        logger.error(f"Error en el programa principal: {e}")

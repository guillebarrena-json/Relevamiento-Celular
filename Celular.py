import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


excel = pd.read_excel('RELEVAMIENTOcelular.xlsx')

claro = excel[excel['Compañía']=='CLARO']
movistar = excel[excel['Compañía']=='MOVISTAR']
personal = excel[excel['Compañía']=='PERSONAL']


import certifi
import urllib3
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

# Esto es por un tema de certificaciones de las URL, mas info en: https://urllib3.readthedocs.io/en/1.26.x/user-guide.html#ssl

for url in excel['Link']:    
    attempts = 3
    for attempt in range(attempts):
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                print(f"Todo bien con esta URL: {url}")
                break 
            else:    
                print(f"Algo salio mal con la siguiente URL: {url}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
        
        if attempt < attempts - 1:
            print(f"Esperando 5 segundos antes de intentar de nuevo la URL: {url}")
            time.sleep(5)
    else:
        print(f"Failed after {attempts} attempts: {url}")


# función scrapear precios

service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

# Claro

planes = []
precios = []
nombres_completos = []
cantidades_de_gigas = []
urls = []

for url in claro['Link']:
    
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)  
        h3_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'CAPACIDAD DE INTERNET Y PRECIO')]")))

        p_element = h3_element.find_element(By.XPATH, "./following-sibling::p[1]")
        text = p_element.text

        # Extrae precio
        precio = re.search(r'\$(\d+(?:\.\d+)?)', text).group(1)
        # Extrae nombre del plan
        plan = text.split('Plan')[1].split('gigas')[0]
        
        nombre_completo = p_element.text       

        # Extrae cantidad de gigas
        cantidad_de_gigas_match = re.search(r'(\d+)\s*gigas', nombre_completo)
        if cantidad_de_gigas_match:
            cantidad_de_gigas = cantidad_de_gigas_match.group(1)  
        else:
            cantidad_de_gigas = None  
        
        planes.append(plan)
        precios.append(precio)
        nombres_completos.append(nombre_completo)
        cantidades_de_gigas.append(cantidad_de_gigas)
        urls.append(url)
        
    except Exception as e:
        print(f"Error processing {url}: {e}")

    time.sleep(2)

df_claro = pd.DataFrame(data={
    'Nombre del Plan': planes,
    'Nombre Completo del Plan': nombres_completos,
    'Precio': precios,
    'Cantidad de Gigas': cantidades_de_gigas,
    'URL': urls
})
driver.quit()
df_claro['Empresa'] = 'Claro'

# Movistar

service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

planes = []
precios = []
nombres_completos = []
cantidades_de_gigas = []
urls = []

for url in movistar['Link']:
    
    driver.get(url)

    try:
        span_element = driver.find_element(By.CLASS_NAME,"pnt-contenedor-detalle-plan")
        plan = span_element.find_element(By.CLASS_NAME, "pnt-detalle-plan-titulo-plan").text

        precio_span = driver.find_element(By.CLASS_NAME, "pnt-precio-detalle-plan")
        precio = precio_span.find_element(By.CLASS_NAME, "m-product-card__sale-item").text
       
        precio = precio.replace("$", "").replace(",", "").strip()

        # Extrae cantidad de gigas
        cantidad_de_gigas_match = re.search(r'(\d+)\s*(?:GB|gb|Gigas|gigas)', plan)
        if cantidad_de_gigas_match:
            cantidad_de_gigas = cantidad_de_gigas_match.group(1)  
        else:
            cantidad_de_gigas = None  
               
        planes.append(plan)
        nombres_completos.append(plan)
        precios.append(precio)
        cantidades_de_gigas.append(cantidad_de_gigas)
        urls.append(url)
        
    except Exception as e:
        print(f"Error processing {url}: {e}")

    time.sleep(2)    

df_movistar = pd.DataFrame(data={
    'Nombre del Plan': planes,
    'Nombre Completo del Plan': nombres_completos,
    'Precio': precios,
    'Cantidad de Gigas': cantidades_de_gigas,
    'URL': urls
})
driver.quit()    
df_movistar['Empresa'] = 'Movistar'


service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

# Personal

planes = []
precios = []
nombres_completos = []
cantidades_de_gigas = []
urls = []

for url in personal['Link']:     
    driver.get(url)

    try:
        if "Error" in driver.title:  # Cambia "Error" por algo específico si es necesario
            print(f"URL {url} no cargó correctamente.")
            continue

        plan = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "OfferDetail_titleOffer__lxNyY"))
        ).text

        # Verifica si existe 'priceBeforeTag'
        if len(driver.find_elements(By.CLASS_NAME, "OfferDetail_priceBeforeTag__G8ARS")) > 0:
            precio = driver.find_element(By.CLASS_NAME, "OfferDetail_priceBeforeTag__G8ARS").text
        else:
            precio = driver.find_element(By.CLASS_NAME, "OfferDetail_priceOfferTag__eQ0kY").text

        precio = precio.replace("$", "").replace(" final por mes", "").strip()

        cantidad_de_gigas_match = re.search(r'(\d+)\s*(?:GB|gb|Gigas|gigas)', plan)
        if cantidad_de_gigas_match:
            cantidad_de_gigas = cantidad_de_gigas_match.group(1)  
        else:
            cantidad_de_gigas = None 

        planes.append(plan)
        nombres_completos.append(plan)
        precios.append(precio)
        cantidades_de_gigas.append(cantidad_de_gigas)
        urls.append(url)

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        print(driver.page_source)  # Ayuda a depurar qué se cargó

    time.sleep(2)    

# Crear DataFrame

df_personal = pd.DataFrame(data={
    'Nombre del Plan': planes,
    'Nombre Completo del Plan': nombres_completos,
    'Precio': precios,
    'Cantidad de Gigas': cantidades_de_gigas,
    'URL': urls
})
driver.quit()
df_personal['Empresa'] = 'Personal'


concatenado = pd.concat([df_claro,df_movistar,df_personal])
concatenado.to_excel('Celular.xlsx')


# funcion descargar pdf's

service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

for index, row in concatenado.iterrows():
    try:
        url = row['URL']
        file_name = row['Nombre del Plan']

        # Open the URL
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        # Simulate Ctrl + P to open the print dialog
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(2)  # Wait for the print dialog to appear

        # Press Enter to confirm print action (opens "Save as PDF" dialog or print dialog depending on system)
        pyautogui.press('enter')
        time.sleep(2)  # Wait for "Save" dialog to appear

        # Write the file name for saving
        pyautogui.write(file_name)
        time.sleep(1)

        # Press Enter to save the file
        pyautogui.press('enter')
        time.sleep(2) 

        print(f"Successfully processed {url} with file name {file_name}")
    
    except Exception as e:
        print(f"Error processing {url} with file name {file_name}: {e}")

# Close the browser once done
driver.quit()

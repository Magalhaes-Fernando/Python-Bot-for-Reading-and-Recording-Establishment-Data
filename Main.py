from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd

driver_path = 'YOUR EDGE WEBDRIVER FOLDER'
edge_options = Options()
edge_options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Substitua pelo caminho correto para o seu Microsoft Edge

# Inicializa o Edge
driver = webdriver.Edge(service=Service(driver_path), options=edge_options)

# Visita a URL
url = "GOOGLE MAPS LINK"
driver.get(url)

# Aguarda para carregar a página
time.sleep(5) # Ajuste conforme necessário

estabelecimentos = []

# Função para extrair os dados da página atual
def extrair_dados():
    elementos = driver.find_elements(By.CSS_SELECTOR, 'div[jscontroller="AtSb"]')
    for elemento in elementos:
        try:
            nome = elemento.find_element(By.CSS_SELECTOR, '.OSrXXb').text
            divs_endereco = elemento.find_elements(By.CSS_SELECTOR, '.rllt__details > div')
            endereco = ''
            for div in divs_endereco:
                if div.get_attribute('childElementCount') == '0':
                    endereco = div.text
                    break
            estabelecimentos.append({'Nome': nome, 'Endereço': endereco})
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")

# Extrai os dados de todas as páginas
try:
    while True:
        extrair_dados()
        proxima_pagina = driver.find_element(By.ID, 'pnnext')
        proxima_pagina.click()
        time.sleep(5) # Aguarda a página carregar
except (NoSuchElementException, ElementClickInterceptedException):
    print("Fim das páginas ou não foi possível clicar em 'Próxima'.")

driver.quit()

# Cria um DataFrame com os dados coletados
df_estabelecimentos = pd.DataFrame(estabelecimentos)

# Exibe ou salva o DataFrame como CSV
df_estabelecimentos.to_csv('dados_estabelecimentos.csv', index=False)

print("Arquivo 'dados_estabelecimentos.csv' criado com sucesso!")
# df_estabelecimentos.to_csv('estabelecimentos.csv', index=False)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd

driver_path = 'C:/WebDriver/msedgedriver.exe'
edge_options = Options()
edge_options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # Substitua pelo caminho correto para o seu Microsoft Edge

# Inicializa o Edge
driver = webdriver.Edge(service=Service(driver_path), options=edge_options)

# Visita a URL
url = "https://www.google.com/search?q=oficinas+itabiura&sca_esv=600400644&biw=1879&bih=1010&tbm=lcl&sxsrf=ACQVn0-qnXxOqec8Uda2WwGwGaBfC9hDKA%3A1705942150743&ei=hpyuZZ79LOfW1sQP3IGC6AE&ved=0ahUKEwie2JvfufGDAxVnq5UCHdyAAB0Q4dUDCAk&uact=5&oq=oficinas+itabiura&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhFvZmljaW5hcyBpdGFiaXVyYTIGEAAYHhgNMggQABgIGB4YDTIKEAAYCBgeGA0YDzIIEAAYCBgeGA0yChAAGAgYHhgNGA9I2c8BUPChAVitzwFwBHgAkAEBmAGKAqAB7xWqAQYwLjE3LjK4AQPIAQD4AQGoAgrCAgQQIxgnwgIGEAAYFhgewgILEAAYgAQYsQMYgwHCAgUQABiABMICChAAGIAEGIoFGEPCAg0QABiABBiKBRhDGLEDwgIIEAAYgAQYsQPCAgcQIxjqAhgnwgIMEAAYgAQYigUYQxgKwgILEAAYgAQYigUYkgPCAggQABiABBjLAcICCBAAGBYYHhgPiAYB&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[-19.613941699999998,-43.2025201],[-19.6393545,-43.237538]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:14"
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

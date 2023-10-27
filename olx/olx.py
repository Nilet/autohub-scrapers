from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import pymongo

# Função para conectar ao MongoDB
def conectar_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["nome_do_seu_banco_de_dados"]
    collection = db["nome_da_sua_colecao"]
    return collection

# Função para ler o arquivo
def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    return open(file_path).read().strip().replace(' ', '%20').split('\n')

# Função para buscar veículos na OLX e armazenar no MongoDB
def OLX_buscaVeiculo(veiculo, driver, collection):
    driver.get(
        f"https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-pr?q={veiculo}")

    title = driver.title
    print(title)

    driver.implicitly_wait(0.5)
    driver.execute_script(
        "document.querySelectorAll('div').forEach(div => div.style.height = '1px')")

    sleep(3)

    source = driver.page_source

    soup = BeautifulSoup(source, 'lxml')
    links = []
    links = soup.find_all(class_='dFgPSB')
    if links == []:
        links = soup.find_all(class_='dPstMh')

    veiculos = []

    for link in links:
        produto = ''
        try:
            produto = link.find('h2').text
        except:
            continue
        url = link.find('a')['href']
        try:
            price = link.find('h3').text.replace('R$ ', '')
        except:
            temp = link.find(class_='old-price')
            if (temp != None):
                price = temp.text.replace('R$ ', '')
            else:
                continue

        img = link.find('source')['srcset']

        veiculos.append(dict(veiculo=produto, url=url, price=price, veiculoImg=img))

    for fusca in veiculos:
        print(fusca)
        # Insira os dados no MongoDB
        inserir_dados_mongodb(collection, fusca["veiculo"], fusca["url"], fusca["price"], fusca["veiculoImg"])
    print()

# Função principal
def main():
    veiculos = lerArquivo("./veiculos.txt")
    collection = conectar_mongodb()
    driver = webdriver.Chrome()  # Substitua pelo seu driver
    for veiculo in veiculos:
        OLX_buscaVeiculo(veiculo, driver, collection)
    driver.quit()

if __name__ == '__main__':
    main()

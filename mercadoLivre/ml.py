#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import os
import pymongo

# Função para conectar ao MongoDB
def conectar_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["autohub"]
    collection = db["veiculos"]
    return collection

def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    return open(file_path).read().strip().replace(' ', '%20').split('\n')

# Função para inserir os dados no MongoDB
def inserir_dados_mongodb(collection, veiculoNome, veiculoUrl, preco, local, veiculoImg):
    data_to_insert = {
        "veiculo": veiculoNome,
        "url": veiculoUrl,
        "price": preco,
        "local": local,
        "veiculoImg": veiculoImg,
        "origem": "ML"
    }
    collection.insert_one(data_to_insert)

def ML_buscaVeiculo(veiculo, collection):
    r = requests.get(
        f"https://lista.mercadolivre.com.br/veiculos-em-parana/{veiculo}_NoIndex_True")
    soup = BeautifulSoup(r.text, 'html.parser')

    containers = soup.find_all(
        'div', {'class': 'ui-search-result__wrapper'})

    veiculos = []
    for container in containers:
        veiculoNome = container.find('h2', {
            'class': 'ui-search-item__title'}).text
        preco = container.find(
            'span', {'class': 'andes-money-amount__fraction'}).text

        veiculoUrl = container.find('a')['href']

        veiculoImg = container.find('img')['data-src']
        local = container.find('span', {
            'class': 'ui-search-item__group__element ui-search-item__location'
        }).text

        veiculos.append(
            dict(veiculo=veiculoNome, url=veiculoUrl, price=preco, local=local, veiculoImg=veiculoImg))

        for fusca in veiculos:
            print(fusca)
            inserir_dados_mongodb(collection, fusca["veiculo"], fusca["url"], fusca["price"], fusca["local"], fusca["veiculoImg"])

    print()

def main():
    veiculos = lerArquivo("./veiculos.txt")
    collection = conectar_mongodb()
    for veiculo in veiculos:
        ML_buscaVeiculo(veiculo, collection)

if __name__ == '__main__':
    main()

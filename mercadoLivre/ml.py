#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from utils.utils import conectar_mongodb, inserir_dados_mongodb, lerArquivo


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
            inserir_dados_mongodb(
                collection, fusca["veiculo"], fusca["url"], fusca["price"], fusca["local"], fusca["veiculoImg"], "ML")

    print()


def main():
    veiculos = lerArquivo("./veiculos.txt")
    collection = conectar_mongodb()
    for veiculo in veiculos:
        ML_buscaVeiculo(veiculo, collection)


if __name__ == '__main__':
    main()

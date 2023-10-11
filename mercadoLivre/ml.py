#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import os


def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    return open(file_path).read().strip().replace(' ', '%20').split('\n')


def ML_buscaVeiculo(veiculo):
    r = requests.get(
        f"https://lista.mercadolivre.com.br/veiculos-em-parana/{veiculo}_NoIndex_True")
    soup = BeautifulSoup(r.text, 'html.parser')

    print(
        f"https://lista.mercadolivre.com.br/veiculos-em-parana/{veiculo}_NoIndex_True")
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
    print()


def main():
    veiculos = lerArquivo("./veiculos.txt")
    for veiculo in veiculos:
        ML_buscaVeiculo(veiculo)


if __name__ == '__main__':
    main()

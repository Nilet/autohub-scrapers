#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests


def lerArquivo(path):
    return open(path).read().strip().replace(' ', '%20').split('\n')


def busca_veiculo(veiculo):
    r = requests.get(
        f"https://lista.mercadolivre.com.br/veiculos-em-parana/{veiculo}_NoIndex_True")
    soup = BeautifulSoup(r.text, 'html.parser')

    print(f"https://lista.mercadolivre.com.br/veiculos-em-parana/{veiculo}_NoIndex_True")
    containers = soup.find_all(
        'div', {'class': 'ui-search-result__wrapper'})

    veiculos = []
    for container in containers:
        veiculoNome = container.find('div', {
            'class': 'ui-search-item__group ui-search-item__group--title shops__items-group'}).text
        preco = container.find(
            'span', {'class': 'andes-money-amount__fraction'}).text

        veiculoUrl = container.find('a')['href']

        veiculoImg = container.find('img')['data-src']
        local = container.find('span', {
            'class': 'ui-search-item__group__element ui-search-item__location shops__items-group-details'
        }).text

        veiculos.append(
            dict(veiculo=veiculoNome, url=veiculoUrl, price=preco, local=local, veiculoImg=veiculoImg))
    for fusca in veiculos:
        print(fusca)
    print()


def main():
    veiculos = lerArquivo("./veiculos.txt")
    for veiculo in veiculos:
        busca_veiculo(veiculo)


if __name__ == '__main__':
    main()

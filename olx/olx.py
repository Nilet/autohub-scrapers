from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from utils.utils import conectar_mongodb, inserir_dados_mongodb, lerArquivo


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
    links = soup.find_all(class_='olx-ad-card olx-ad-card--vertical')
    if links == []:
        links = soup.find_all(class_='dPstMh')

    veiculos = []

    for link in links:
        produto = ''
        try:
            produto = link.find('h2').text
        except:
            continue
        url = link.find(class_='olx-ad-card__title-link')['href']
        try:
            price = int(link.find('h3').text.replace(
                'R$ ', '').replace(".", ""))
        except:
            temp = link.find(class_='olx-ad-card__price')
            if (temp is not None):
                price = temp.text.replace('R$ ', '')
            else:
                continue
        local = ""
        try:
            local = link.find(
                class_="olx-ad-card__location-date-container").find("p").text
        except:
            pass

        km = 0
        ano = 0
        try:
            dados = link.find_all(class_='olx-ad-card__labels-item')
            km = int(dados[0].text.replace(".", "").replace(" km", ""))
            ano = int(dados[1].text)
        except:
            km = 0
            ano = 0

        img = link.find('source')['srcset']

        veiculos.append(dict(veiculo=produto, url=url,
                        price=price, veiculoImg=img, local=local,
                             km=km, ano=ano))

    for fusca in veiculos:
        print(fusca)
        inserir_dados_mongodb(
            collection, fusca["veiculo"], fusca["url"], fusca["price"], fusca["local"], fusca["veiculoImg"],
            fusca["km"], fusca["ano"], "OLX")
    print()


def main():
    veiculos = lerArquivo("./veiculos.txt")
    collection = conectar_mongodb()
    driver = webdriver.Chrome()
    for veiculo in veiculos:
        OLX_buscaVeiculo(veiculo, driver, collection)
    driver.quit()


if __name__ == '__main__':
    main()

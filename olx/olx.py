from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os


def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    return open(file_path).read().strip().replace(' ', '%20').split('\n')


def buscaVeiculo(veiculo):

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
        print(img)
        veiculos.append(dict(veiculo=produto, url=url, price=price))

    for fusca in veiculos:
        print(fusca)
    print()


veiculos = lerArquivo("veiculos.txt")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--windows-size=1920x1080')
driver = webdriver.Chrome()
for veiculo in veiculos:
    buscaVeiculo(veiculo)
driver.quit()

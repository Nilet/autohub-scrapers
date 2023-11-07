import threading
import concurrent.futures
from selenium import webdriver
from mercadoLivre.ml import ML_buscaVeiculo
from olx.olx import OLX_buscaVeiculo
from utils.utils import conectar_mongodb, lerArquivo


class ScrapeThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.veiculo = url

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--windows-size=1920x1080')
        driver = webdriver.Chrome(options=options)
        OLX_buscaVeiculo(self.veiculo, driver, collection)
        ML_buscaVeiculo(self.veiculo, collection)
        driver.close()


if __name__ == "__main__":
    veiculos = lerArquivo("veiculos.txt")
    collection = conectar_mongodb()
    print("Iniciando")
    threads = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        for veiculo in veiculos:
            print(veiculo)
            t = ScrapeThread(veiculo)
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

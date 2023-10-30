import threading
from selenium import webdriver
from mercadoLivre.ml import ML_buscaVeiculo
from olx.olx import OLX_buscaVeiculo
import os
import pymongo


def conectar_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["autohub"]
    collection = db["veiculos"]
    return collection

class ScrapeThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.veiculo = url

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--windows-size=1920x1080')
        driver = webdriver.Chrome(options=options)
        OLX_buscaVeiculo(self.veiculo, driver, collection)
        ML_buscaVeiculo(self.veiculo, collection)
        driver.close()


def lerArquivo(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    return open(file_path).read().strip().replace(' ', '%20').split('\n')


if __name__ == "__main__":
    veiculos = lerArquivo("veiculos.txt")
    collection = conectar_mongodb()
    threads = []

    for veiculo in veiculos:
        t = ScrapeThread(veiculo)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
